import argparse
import json
from pathlib import Path
from typing import Optional

from .agent import OllamaChatClient, RagAgent, evaluate_answers, load_control_questions
from .embeddings import get_embedder
from .pipeline import build_index, compare_indexes, render_markdown_report
from .vector_store import VectorIndex


def main() -> None:
    parser = argparse.ArgumentParser(description="Build and compare local RAG indexes with Ollama embeddings.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_build_parser(subparsers)
    add_build_all_parser(subparsers)
    add_compare_parser(subparsers)
    add_search_parser(subparsers)
    add_answer_parser(subparsers)
    add_evaluate_answers_parser(subparsers)

    args = parser.parse_args()
    if args.command == "build":
        run_build(args)
    elif args.command == "build-all":
        for strategy in ["fixed", "structural"]:
            args.strategy = strategy
            run_build(args)
    elif args.command == "compare":
        run_compare(args)
    elif args.command == "search":
        run_search(args)
    elif args.command == "answer":
        run_answer(args)
    elif args.command == "evaluate-answers":
        run_evaluate_answers(args)


def add_common_embedding_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--embedder", choices=["ollama", "hash"], default="ollama")
    parser.add_argument("--model", default=None, help="Ollama embedding model. Defaults to qwen3-embedding.")
    parser.add_argument("--ollama-url", default="http://localhost:11434")
    parser.add_argument("--batch-size", type=int, default=16)
    parser.add_argument("--timeout", type=int, default=180)


def add_build_parser(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser("build", help="Build one index.")
    parser.add_argument("--corpus", type=Path, default=Path("corpus"))
    parser.add_argument("--out", type=Path, default=Path("indexes"))
    parser.add_argument("--strategy", choices=["fixed", "structural"], required=True)
    parser.add_argument("--fixed-chars", type=int, default=1200)
    parser.add_argument("--fixed-overlap", type=int, default=180)
    parser.add_argument("--structural-max-chars", type=int, default=1800)
    parser.add_argument("--structural-overlap", type=int, default=160)
    add_common_embedding_args(parser)


def add_build_all_parser(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser("build-all", help="Build fixed and structural indexes.")
    parser.add_argument("--corpus", type=Path, default=Path("corpus"))
    parser.add_argument("--out", type=Path, default=Path("indexes"))
    parser.add_argument("--fixed-chars", type=int, default=1200)
    parser.add_argument("--fixed-overlap", type=int, default=180)
    parser.add_argument("--structural-max-chars", type=int, default=1800)
    parser.add_argument("--structural-overlap", type=int, default=160)
    add_common_embedding_args(parser)


def add_compare_parser(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser("compare", help="Compare fixed and structural indexes.")
    parser.add_argument("--index-root", type=Path, default=Path("indexes"))
    parser.add_argument("--strategies", default="fixed,structural")
    parser.add_argument("--queries", type=Path, default=None)
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument("--search-mode", choices=["dense", "hybrid"], default="dense")
    parser.add_argument("--report", type=Path, default=Path("reports/chunking_comparison.md"))
    parser.add_argument("--json-report", type=Path, default=Path("reports/chunking_comparison.json"))
    add_common_embedding_args(parser)


def add_search_parser(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser("search", help="Search an index.")
    parser.add_argument("--index", type=Path, required=True)
    parser.add_argument("--query", required=True)
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument("--search-mode", choices=["dense", "hybrid"], default="dense")
    add_common_embedding_args(parser)


def add_common_agent_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--index", type=Path, default=Path("indexes-real-qwen/structural"))
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument("--search-mode", choices=["dense", "hybrid"], default="hybrid")
    parser.add_argument("--chat-model", default="qwen2.5:7b", help="Ollama chat model.")
    parser.add_argument("--chat-url", default="http://localhost:11434")
    parser.add_argument("--max-context-chars", type=int, default=8000)
    add_common_embedding_args(parser)


def add_answer_parser(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser("answer", help="Answer a question with or without RAG.")
    parser.add_argument("--query", required=True)
    parser.add_argument("--mode", choices=["rag", "plain", "compare"], default="compare")
    parser.add_argument("--json", action="store_true", help="Print JSON instead of text.")
    add_common_agent_args(parser)


def add_evaluate_answers_parser(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser("evaluate-answers", help="Compare plain vs RAG answers on a control set.")
    parser.add_argument("--questions", type=Path, default=Path("evaluation/rag_control_questions.json"))
    parser.add_argument("--report", type=Path, default=Path("reports/rag_answer_comparison.json"))
    add_common_agent_args(parser)


def make_embedder(args: argparse.Namespace, default_model: Optional[str] = None):
    return get_embedder(
        args.embedder,
        model=args.model or default_model,
        ollama_url=args.ollama_url,
        batch_size=args.batch_size,
        timeout=args.timeout,
    )


def run_build(args: argparse.Namespace) -> None:
    embedder = make_embedder(args)
    manifest = build_index(
        corpus_dir=args.corpus,
        out_root=args.out,
        strategy=args.strategy,
        embedder=embedder,
        fixed_chars=args.fixed_chars,
        fixed_overlap=args.fixed_overlap,
        structural_max_chars=args.structural_max_chars,
        structural_overlap=args.structural_overlap,
    )
    print(json.dumps({"strategy": args.strategy, "manifest": manifest}, indent=2))


def run_compare(args: argparse.Namespace) -> None:
    strategies = [item.strip() for item in args.strategies.split(",") if item.strip()]
    default_model = model_from_first_manifest(args.index_root, strategies)
    embedder = make_embedder(args, default_model=default_model)
    report = compare_indexes(
        index_root=args.index_root,
        strategies=strategies,
        embedder=embedder,
        queries_path=args.queries,
        top_k=args.top_k,
        search_mode=args.search_mode,
    )
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.json_report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(render_markdown_report(report), encoding="utf-8")
    args.json_report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("Wrote %s" % args.report)
    print("Wrote %s" % args.json_report)


def run_search(args: argparse.Namespace) -> None:
    index = VectorIndex(args.index)
    default_model = index.manifest.get("model")
    embedder = make_embedder(args, default_model=default_model)
    vector = embedder.embed([args.query])
    results = index.search(vector, top_k=args.top_k, mode=args.search_mode, query_text=args.query)
    for rank, result in enumerate(results, start=1):
        chunk = result.chunk
        preview = " ".join(str(chunk.get("text", "")).split())[:260]
        print(
            "[%d] score=%.4f dense=%.4f lexical=%.4f source=%s section=%s chunk_id=%s"
            % (
                rank,
                result.score,
                result.dense_score,
                result.lexical_score or 0.0,
                chunk.get("source"),
                chunk.get("section"),
                chunk.get("chunk_id"),
            )
        )
        print("    %s" % preview)


def make_agent(args: argparse.Namespace) -> RagAgent:
    index = VectorIndex(args.index)
    default_model = index.manifest.get("model")
    embedder = make_embedder(args, default_model=default_model)
    chat_client = OllamaChatClient(model=args.chat_model, base_url=args.chat_url, timeout=args.timeout)
    return RagAgent(
        chat_client=chat_client,
        embedder=embedder,
        index=index,
        top_k=args.top_k,
        search_mode=args.search_mode,
        max_context_chars=args.max_context_chars,
    )


def run_answer(args: argparse.Namespace) -> None:
    agent = make_agent(args)
    if args.mode == "compare":
        payload = agent.compare(args.query)
    else:
        payload = agent.answer(args.query, use_rag=args.mode == "rag").to_json()

    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return

    if args.mode == "compare":
        print("Question: %s" % payload["question"])
        print("\n--- Without RAG ---\n%s" % payload["plain"]["answer"])
        print("\n--- With RAG ---\n%s" % payload["rag"]["answer"])
        print("\nSources:")
        for source in payload["rag"]["sources"]:
            print("[%d] %s / %s score=%.4f" % (source["rank"], source["source"], source["section"], source["score"]))
    else:
        print(payload["answer"])
        if payload["sources"]:
            print("\nSources:")
            for source in payload["sources"]:
                print("[%d] %s / %s score=%.4f" % (source["rank"], source["source"], source["section"], source["score"]))


def run_evaluate_answers(args: argparse.Namespace) -> None:
    agent = make_agent(args)
    questions = load_control_questions(args.questions)
    report = evaluate_answers(agent, questions)
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("Wrote %s" % args.report)
    print("RAG source hit@5: %s" % report["summary"]["rag_source_hit_at_5"])
    print("Plain expectation coverage: %s" % report["summary"]["plain_expectation_coverage"])
    print("RAG expectation coverage: %s" % report["summary"]["rag_expectation_coverage"])


def model_from_first_manifest(index_root: Path, strategies) -> Optional[str]:
    for strategy in strategies:
        manifest_path = index_root / strategy / "manifest.json"
        if manifest_path.exists():
            payload = json.loads(manifest_path.read_text(encoding="utf-8"))
            return payload.get("model")
    return None


if __name__ == "__main__":
    main()
