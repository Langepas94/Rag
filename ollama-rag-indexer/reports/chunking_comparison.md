# Chunking Strategy Comparison

Generated at: `2026-06-29T13:30:50Z`

## Chunk Statistics

| Strategy | Chunks | Avg chars | Min | Max | Section coverage | Backend |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| fixed | 199 | 1140.52 | 194 | 1199 | 1.0 | faiss |
| structural | 176 | 1160.82 | 127 | 1799 | 1.0 | faiss |

## Retrieval Metrics

| Strategy | Queries | hit@1 | hit@3 | hit@5 | section@3 | MRR |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| fixed | 10 | 0.4 | 0.6 | 0.7 | 0.5 | 0.525 |
| structural | 10 | 0.2 | 0.6 | 0.8 | 0.7 | 0.4117 |

## Query Details

### fixed

- `How are source title section and chunk_id stored for every chunk?` -> source rank: `None`, section rank: `None`
  - top1: `code/sample_indexing_service.py` / `function build_stage_12` score `0.3662`
- `Which strategy uses bounded character windows with overlap?` -> source rank: `None`, section rank: `3`
  - top1: `articles/retrieval_architecture.md` / `Section 18: Chunk Metadata` score `0.2099`
- `What boundaries does structural chunking use before fallback splitting?` -> source rank: `None`, section rank: `3`
  - top1: `articles/retrieval_architecture.md` / `Section 27: Fixed Windows` score `0.1551`
- `Where are hit at k reciprocal rank and section accuracy described?` -> source rank: `1`, section rank: `3`
  - top1: `articles/chunking_evaluation.md` / `Section 22: Vector Storage` score `0.3665`
- `Which notes describe FAISS and NumPy vectors as storage backends?` -> source rank: `2`, section rank: `3`
  - top1: `articles/chunking_evaluation.md` / `Section 13: Embedding Backend` score `0.2309`
- `What code function applies indexing stage 12 with metadata validation?` -> source rank: `1`, section rank: `None`
  - top1: `code/sample_indexing_service.py` / `function build_stage_07` score `0.2729`
- `Which PDF chapter explains operational checks for document count and metadata coverage?` -> source rank: `1`, section rank: `1`
  - top1: `papers/operations_playbook.pdf` / `page 12` score `0.2734`
- `How does the embedding backend request local vectors from Ollama?` -> source rank: `4`, section rank: `None`
  - top1: `papers/operations_playbook.pdf` / `page 3` score `0.347`
- `Why can chunks that are too small lose setup definitions and examples?` -> source rank: `2`, section rank: `None`
  - top1: `papers/operations_playbook.pdf` / `page 6` score `0.3141`
- `What service record keeps source title section and metadata fields?` -> source rank: `1`, section rank: `None`
  - top1: `code/sample_indexing_service.py` / `function build_stage_23` score `0.5976`

### structural

- `How are source title section and chunk_id stored for every chunk?` -> source rank: `None`, section rank: `None`
  - top1: `code/sample_indexing_service.py` / `function build_stage_18` score `0.3264`
- `Which strategy uses bounded character windows with overlap?` -> source rank: `5`, section rank: `3`
  - top1: `papers/operations_playbook.pdf` / `page 5` score `0.2274`
- `What boundaries does structural chunking use before fallback splitting?` -> source rank: `3`, section rank: `3`
  - top1: `papers/operations_playbook.pdf` / `page 2` score `0.2021`
- `Where are hit at k reciprocal rank and section accuracy described?` -> source rank: `3`, section rank: `2`
  - top1: `papers/operations_playbook.pdf` / `page 7` score `0.415`
- `Which notes describe FAISS and NumPy vectors as storage backends?` -> source rank: `2`, section rank: `1`
  - top1: `README.md` / `Vector Storage` score `0.1905`
- `What code function applies indexing stage 12 with metadata validation?` -> source rank: `1`, section rank: `2`
  - top1: `code/sample_indexing_service.py` / `function build_stage_10` score `0.2537`
- `Which PDF chapter explains operational checks for document count and metadata coverage?` -> source rank: `2`, section rank: `2`
  - top1: `README.md` / `Operational Checks` score `0.2339`
- `How does the embedding backend request local vectors from Ollama?` -> source rank: `4`, section rank: `2`
  - top1: `papers/operations_playbook.pdf` / `page 6` score `0.3569`
- `Why can chunks that are too small lose setup definitions and examples?` -> source rank: `None`, section rank: `None`
  - top1: `papers/operations_playbook.pdf` / `page 14` score `0.3546`
- `What service record keeps source title section and metadata fields?` -> source rank: `1`, section rank: `None`
  - top1: `code/sample_indexing_service.py` / `function build_stage_18` score `0.5477`

## Interpretation

- Fixed chunking is expected to produce more uniform chunk sizes and predictable overlap.
- Structural chunking is expected to preserve headings, pages, functions, and sections more often.
- Prefer the strategy with stronger retrieval metrics unless its chunk sizes are too uneven for the target context window.
