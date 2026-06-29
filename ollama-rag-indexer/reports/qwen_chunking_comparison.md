# Chunking Strategy Comparison

Generated at: `2026-06-29T16:13:27Z`

## Chunk Statistics

| Strategy | Chunks | Avg chars | Min | Max | Section coverage | Backend |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| fixed | 199 | 1140.52 | 194 | 1199 | 1.0 | faiss |
| structural | 176 | 1160.82 | 127 | 1799 | 1.0 | faiss |

## Retrieval Metrics

| Strategy | Queries | hit@1 | hit@3 | hit@5 | section@3 | MRR |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| fixed | 10 | 0.4 | 0.5 | 0.7 | 0.4 | 0.4833 |
| structural | 10 | 0.2 | 0.6 | 0.8 | 0.8 | 0.4283 |

## Query Details

### fixed

- `How are source title section and chunk_id stored for every chunk?` -> source rank: `None`, section rank: `None`
  - top1: `papers/operations_playbook.pdf` / `page 9` score `0.7414`
- `Which strategy uses bounded character windows with overlap?` -> source rank: `None`, section rank: `1`
  - top1: `articles/chunking_evaluation.md` / `Section 19: Fixed Windows` score `0.6349`
- `What boundaries does structural chunking use before fallback splitting?` -> source rank: `None`, section rank: `None`
  - top1: `papers/operations_playbook.pdf` / `page 14` score `0.6632`
- `Where are hit at k reciprocal rank and section accuracy described?` -> source rank: `4`, section rank: `3`
  - top1: `papers/operations_playbook.pdf` / `page 11` score `0.7161`
- `Which notes describe FAISS and NumPy vectors as storage backends?` -> source rank: `1`, section rank: `1`
  - top1: `articles/retrieval_architecture.md` / `Section 06: Vector Storage` score `0.7617`
- `What code function applies indexing stage 12 with metadata validation?` -> source rank: `1`, section rank: `4`
  - top1: `code/sample_indexing_service.py` / `function build_stage_02` score `0.7127`
- `Which PDF chapter explains operational checks for document count and metadata coverage?` -> source rank: `3`, section rank: `3`
  - top1: `articles/chunking_evaluation.md` / `Section 31: Retrieval Metrics` score `0.7049`
- `How does the embedding backend request local vectors from Ollama?` -> source rank: `4`, section rank: `None`
  - top1: `papers/operations_playbook.pdf` / `page 3` score `0.7866`
- `Why can chunks that are too small lose setup definitions and examples?` -> source rank: `1`, section rank: `None`
  - top1: `articles/chunking_evaluation.md` / `Section 03: Fixed Windows` score `0.6017`
- `What service record keeps source title section and metadata fields?` -> source rank: `1`, section rank: `None`
  - top1: `code/sample_indexing_service.py` / `function build_stage_03` score `0.6315`

### structural

- `How are source title section and chunk_id stored for every chunk?` -> source rank: `4`, section rank: `2`
  - top1: `code/sample_indexing_service.py` / `class ChunkRecord` score `0.7763`
- `Which strategy uses bounded character windows with overlap?` -> source rank: `2`, section rank: `2`
  - top1: `papers/operations_playbook.pdf` / `page 2` score `0.664`
- `What boundaries does structural chunking use before fallback splitting?` -> source rank: `2`, section rank: `2`
  - top1: `papers/operations_playbook.pdf` / `page 9` score `0.6835`
- `Where are hit at k reciprocal rank and section accuracy described?` -> source rank: `2`, section rank: `2`
  - top1: `papers/operations_playbook.pdf` / `page 7` score `0.7235`
- `Which notes describe FAISS and NumPy vectors as storage backends?` -> source rank: `5`, section rank: `1`
  - top1: `articles/chunking_evaluation.md` / `Section 22: Vector Storage` score `0.8028`
- `What code function applies indexing stage 12 with metadata validation?` -> source rank: `1`, section rank: `1`
  - top1: `code/sample_indexing_service.py` / `function build_stage_12` score `0.6901`
- `Which PDF chapter explains operational checks for document count and metadata coverage?` -> source rank: `None`, section rank: `None`
  - top1: `articles/chunking_evaluation.md` / `Section 16: Operational Checks` score `0.7278`
- `How does the embedding backend request local vectors from Ollama?` -> source rank: `None`, section rank: `2`
  - top1: `papers/operations_playbook.pdf` / `page 6` score `0.7961`
- `Why can chunks that are too small lose setup definitions and examples?` -> source rank: `3`, section rank: `None`
  - top1: `papers/operations_playbook.pdf` / `page 2` score `0.592`
- `What service record keeps source title section and metadata fields?` -> source rank: `1`, section rank: `1`
  - top1: `code/sample_indexing_service.py` / `class ChunkRecord` score `0.6266`

## Interpretation

- Fixed chunking is expected to produce more uniform chunk sizes and predictable overlap.
- Structural chunking is expected to preserve headings, pages, functions, and sections more often.
- Prefer the strategy with stronger retrieval metrics unless its chunk sizes are too uneven for the target context window.
