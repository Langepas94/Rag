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
over source paths, sections, and chunk text. Dense search remains the default
because it performed best on the current qwen evaluation set.

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
3. merge ranked chunk context with the question
4. ask the chat LLM to answer using that context

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
