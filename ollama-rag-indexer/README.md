# Ollama RAG Indexer

Local document indexing pipeline with two chunking strategies, Ollama embeddings,
metadata-rich chunks, and a reusable comparison report.

The project handles Markdown, plain text, source code, and PDF files. It writes
one index per strategy:

- `index.faiss` when `faiss-cpu` is installed
- `vectors.npy` as a portable fallback
- `chunks.jsonl` with chunk text and metadata
- `manifest.json` with build settings and statistics

## Quick Start

Install dependencies:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -e ".[dev,pdf,faiss]"
```

If FAISS is unavailable for your Python/platform, install without the `faiss`
extra. The project will still save a local NumPy/JSON index:

```bash
.venv/bin/python -m pip install -e ".[dev,pdf]"
```

Create a sample corpus with README, articles, code, and PDF material:

```bash
.venv/bin/python scripts/create_sample_corpus.py
```

Start Ollama and pull an embedding model:

```bash
ollama serve
ollama pull qwen3-embedding
```

Build both indexes:

```bash
.venv/bin/rag-indexer build-all --corpus corpus --out indexes --model qwen3-embedding
```

Compare the strategies:

```bash
.venv/bin/rag-indexer compare \
  --index-root indexes \
  --queries evaluation/queries.json \
  --report reports/chunking_comparison.md \
  --model qwen3-embedding
```

For the real `tg-agent` + `open-meteo-mcp` corpus:

```bash
.venv/bin/rag-indexer build-all \
  --corpus corpus-real \
  --out indexes-real-qwen \
  --model qwen3-embedding \
  --batch-size 4 \
  --timeout 600

.venv/bin/rag-indexer compare \
  --index-root indexes-real-qwen \
  --queries evaluation/real_project_queries.json \
  --model qwen3-embedding \
  --batch-size 4 \
  --timeout 600 \
  --search-mode dense \
  --report reports/real_qwen_chunking_comparison.md
```

Search:

```bash
.venv/bin/rag-indexer search \
  --index indexes/structural \
  --query "How should metadata be attached to each chunk?" \
  --model qwen3-embedding
```

Use `--search-mode hybrid` to blend dense vector search with lexical matching
over source paths, sections, and chunk text. Use `--search-mode lexical` on a
small VPS when the qwen embedding model is too large for RAM: it searches the
already built `chunks.jsonl` text and source metadata without calling the
embedding model for every question. Dense search remains the default because it
performed best on the current qwen evaluation set.

Answer with the same LLM in two modes:

```bash
.venv/bin/rag-indexer answer \
  --index indexes-real-qwen/structural \
  --query "How does the Telegram bot connect to MCP servers at runtime?" \
  --mode compare \
  --model qwen3-embedding \
  --chat-model qwen2.5:7b
```

`--mode plain` sends only the question to the chat model. `--mode rag` performs:

1. embed the question
2. search relevant chunks in the local vector index
3. optionally rewrite the query for lexical/hybrid matching
4. retrieve a larger candidate set
5. drop candidates below the configured similarity threshold
6. merge the remaining ranked chunk context with the question
7. ask the chat LLM to answer using that context

Tune the second-stage filter with:

```bash
.venv/bin/rag-indexer answer \
  --index indexes-real-qwen/structural \
  --query "How does the Telegram bot connect to MCP servers at runtime?" \
  --mode rag \
  --model qwen3-embedding \
  --search-mode hybrid \
  --candidate-k 12 \
  --top-k 5 \
  --similarity-threshold 0.8 \
  --rewrite-query
```

Compare baseline retrieval against rewrite + filtering without running the chat
model:

```bash
.venv/bin/rag-indexer compare-modes \
  --index-root indexes-real-qwen \
  --queries evaluation/real_project_queries.json \
  --model qwen3-embedding \
  --search-mode hybrid \
  --candidate-k 12 \
  --top-k 5 \
  --similarity-threshold 0.8 \
  --report reports/rag_mode_comparison.md
```

`candidate-k` is the number of retrieved results before filtering, while
`top-k` is the maximum number of results passed to the answer context after
filtering. Query rewrite is deliberately heuristic and fast: the original query
is still used for the embedding vector, while the rewritten query helps the
hybrid lexical stage match source paths and code identifiers.

Run the 10-question control set:

```bash
.venv/bin/rag-indexer evaluate-answers \
  --index indexes-real-qwen/structural \
  --questions evaluation/rag_control_questions.json \
  --report reports/rag_answer_comparison.json \
  --model qwen3-embedding \
  --chat-model qwen2.5:7b
```

The report stores both answers for every question, retrieved sources, source
hit@5 for RAG, and simple expectation coverage for plain vs RAG answers. A
Telegram bot can call the same `RagAgent`/CLI contract as a client: send a user
question with mode `plain` or `rag`, then return `answer` plus `sources`.

## Telegram Bot Integration

The `corpus-real/tg-agent` bot has a slash-command bridge to this RAG pipeline.
The command `/rag` controls how ordinary Telegram messages are answered:

```text
/rag status   show mode, RAG workdir, Python path, and index path
/rag on       use RAG for following free-text messages
/rag off      use the normal MCP/travel assistant
/rag compare  answer each following question both without RAG and with RAG
```

At runtime the Rust bot starts the Python CLI:

```bash
python -m rag_indexer.cli answer --mode rag|plain|compare ...
```

Set these environment variables for a server/systemd deployment:

```bash
RAG_WORKDIR=/opt/ollama-rag-indexer
RAG_PYTHON=/opt/ollama-rag-indexer/.venv/bin/python
RAG_INDEX=/opt/ollama-rag-indexer/indexes-real-qwen/structural
RAG_EMBED_MODEL=qwen3-embedding
RAG_CHAT_MODEL=qwen2.5:7b
RAG_SEARCH_MODE=hybrid
```

For a low-memory VPS, keep the prebuilt qwen index but switch retrieval to
lexical search and use a smaller chat model:

```bash
RAG_INDEX=/opt/ollama-rag-indexer/indexes-real-qwen/structural
RAG_CHAT_MODEL=qwen2.5:0.5b
RAG_SEARCH_MODE=lexical
```

In this mode the server does not recalculate embeddings for the question. It
uses the already uploaded chunk database and matches by words, file paths,
sections, and code identifiers.

Optional retrieval tuning:

```bash
RAG_REWRITE_QUERY=1
RAG_TOP_K=5
RAG_CANDIDATE_K=12
RAG_SIMILARITY_THRESHOLD=0.8
```

For a customer demo in Telegram, use `/rag compare`, ask one of the control
questions from `evaluation/rag_control_questions.json`, and show that the RAG
answer includes a `Sources` block while the plain answer does not.

For a smoke run without Ollama, use the deterministic hash embedder:

```bash
.venv/bin/rag-indexer build-all --corpus corpus --out indexes --embedder hash
.venv/bin/rag-indexer compare --index-root indexes --queries evaluation/queries.json --embedder hash
```

## Chunking Strategies

### Fixed

Splits every document into windows of stable character size with overlap. This
is simple, predictable, and easy to tune, but can cut through a heading,
paragraph, or function body.

### Structural

Splits by natural boundaries first:

- Markdown headings
- text section headings
- PDF pages
- source code classes and functions

Large structural sections are then split with the same bounded-window fallback,
so chunks stay within retrieval-friendly limits.

## Comparison

The comparison command reports:

- chunk count
- average/min/max chunk size
- estimated token count
- section metadata coverage
- chunks per source
- optional retrieval metrics from a query set:
  - `hit@1`, `hit@3`, `hit@5`
  - MRR
  - source and section accuracy

The only variable between the two indexes should be the chunking strategy. The
corpus, embedding model, vector backend, and top-k settings should stay the same.
