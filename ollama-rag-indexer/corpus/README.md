# Local RAG Corpus

## Ingestion Contract

This readme note describes loaders preserve source paths, document titles, page numbers,
and a stable kind field. The section is intentionally verbose so that indexing tests
have enough material to form realistic chunks. A retrieval system should keep the
relationship between the user question, the original source, and the surrounding section
visible. When a chunk crosses a boundary, the answer may still be relevant, but the
metadata becomes less precise for review and citation. When a chunk is too small, it can
lose setup, definitions, and examples that make the result useful to a reader. The
preferred implementation records offsets, stable identifiers, and plain text so that a
later answer can cite the exact file or page. Topic marker 001 repeats the phrase
ingestion contract to make evaluation queries deterministic without hiding the normal
prose around it.

## Chunk Metadata

This readme note describes every chunk carries source, title, section, chunk_id,
offsets, and page information when available. The section is intentionally verbose so
that indexing tests have enough material to form realistic chunks. A retrieval system
should keep the relationship between the user question, the original source, and the
surrounding section visible. When a chunk crosses a boundary, the answer may still be
relevant, but the metadata becomes less precise for review and citation. When a chunk is
too small, it can lose setup, definitions, and examples that make the result useful to a
reader. The preferred implementation records offsets, stable identifiers, and plain text
so that a later answer can cite the exact file or page. Topic marker 002 repeats the
phrase chunk metadata to make evaluation queries deterministic without hiding the normal
prose around it.

## Fixed Windows

This readme note describes fixed chunking uses bounded character windows with overlap
and whitespace-aware break points. The section is intentionally verbose so that indexing
tests have enough material to form realistic chunks. A retrieval system should keep the
relationship between the user question, the original source, and the surrounding section
visible. When a chunk crosses a boundary, the answer may still be relevant, but the
metadata becomes less precise for review and citation. When a chunk is too small, it can
lose setup, definitions, and examples that make the result useful to a reader. The
preferred implementation records offsets, stable identifiers, and plain text so that a
later answer can cite the exact file or page. Topic marker 003 repeats the phrase fixed
windows to make evaluation queries deterministic without hiding the normal prose around
it.

## Structural Boundaries

This readme note describes structural chunking starts from headings, pages, files,
classes, and functions. The section is intentionally verbose so that indexing tests have
enough material to form realistic chunks. A retrieval system should keep the
relationship between the user question, the original source, and the surrounding section
visible. When a chunk crosses a boundary, the answer may still be relevant, but the
metadata becomes less precise for review and citation. When a chunk is too small, it can
lose setup, definitions, and examples that make the result useful to a reader. The
preferred implementation records offsets, stable identifiers, and plain text so that a
later answer can cite the exact file or page. Topic marker 004 repeats the phrase
structural boundaries to make evaluation queries deterministic without hiding the normal
prose around it.

## Embedding Backend

This readme note describes Ollama embeddings are requested through the local HTTP API
and stored as normalized vectors. The section is intentionally verbose so that indexing
tests have enough material to form realistic chunks. A retrieval system should keep the
relationship between the user question, the original source, and the surrounding section
visible. When a chunk crosses a boundary, the answer may still be relevant, but the
metadata becomes less precise for review and citation. When a chunk is too small, it can
lose setup, definitions, and examples that make the result useful to a reader. The
preferred implementation records offsets, stable identifiers, and plain text so that a
later answer can cite the exact file or page. Topic marker 005 repeats the phrase
embedding backend to make evaluation queries deterministic without hiding the normal
prose around it.

## Vector Storage

This readme note describes FAISS is used when installed and NumPy vectors remain
available as a portable fallback. The section is intentionally verbose so that indexing
tests have enough material to form realistic chunks. A retrieval system should keep the
relationship between the user question, the original source, and the surrounding section
visible. When a chunk crosses a boundary, the answer may still be relevant, but the
metadata becomes less precise for review and citation. When a chunk is too small, it can
lose setup, definitions, and examples that make the result useful to a reader. The
preferred implementation records offsets, stable identifiers, and plain text so that a
later answer can cite the exact file or page. Topic marker 006 repeats the phrase vector
storage to make evaluation queries deterministic without hiding the normal prose around
it.

## Retrieval Metrics

This readme note describes comparison uses hit at k, reciprocal rank, source accuracy,
and section accuracy. The section is intentionally verbose so that indexing tests have
enough material to form realistic chunks. A retrieval system should keep the
relationship between the user question, the original source, and the surrounding section
visible. When a chunk crosses a boundary, the answer may still be relevant, but the
metadata becomes less precise for review and citation. When a chunk is too small, it can
lose setup, definitions, and examples that make the result useful to a reader. The
preferred implementation records offsets, stable identifiers, and plain text so that a
later answer can cite the exact file or page. Topic marker 007 repeats the phrase
retrieval metrics to make evaluation queries deterministic without hiding the normal
prose around it.

## Operational Checks

This readme note describes the pipeline verifies document count, estimated pages, chunk
counts, and metadata coverage. The section is intentionally verbose so that indexing
tests have enough material to form realistic chunks. A retrieval system should keep the
relationship between the user question, the original source, and the surrounding section
visible. When a chunk crosses a boundary, the answer may still be relevant, but the
metadata becomes less precise for review and citation. When a chunk is too small, it can
lose setup, definitions, and examples that make the result useful to a reader. The
preferred implementation records offsets, stable identifiers, and plain text so that a
later answer can cite the exact file or page. Topic marker 008 repeats the phrase
operational checks to make evaluation queries deterministic without hiding the normal
prose around it.

