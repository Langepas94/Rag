# Chunking Evaluation Field Guide

## Section 01: Ingestion Contract

This evaluation note describes loaders preserve source paths, document titles, page
numbers, and a stable kind field. The section is intentionally verbose so that indexing
tests have enough material to form realistic chunks. A retrieval system should keep the
relationship between the user question, the original source, and the surrounding section
visible. When a chunk crosses a boundary, the answer may still be relevant, but the
metadata becomes less precise for review and citation. When a chunk is too small, it can
lose setup, definitions, and examples that make the result useful to a reader. The
preferred implementation records offsets, stable identifiers, and plain text so that a
later answer can cite the exact file or page. Topic marker 001 repeats the phrase
ingestion contract to make evaluation queries deterministic without hiding the normal
prose around it.

This evaluation-deep-dive note describes loaders preserve source paths, document titles,
page numbers, and a stable kind field. The section is intentionally verbose so that
indexing tests have enough material to form realistic chunks. A retrieval system should
keep the relationship between the user question, the original source, and the
surrounding section visible. When a chunk crosses a boundary, the answer may still be
relevant, but the metadata becomes less precise for review and citation. When a chunk is
too small, it can lose setup, definitions, and examples that make the result useful to a
reader. The preferred implementation records offsets, stable identifiers, and plain text
so that a later answer can cite the exact file or page. Topic marker 033 repeats the
phrase ingestion contract to make evaluation queries deterministic without hiding the
normal prose around it.

## Section 02: Chunk Metadata

This evaluation note describes every chunk carries source, title, section, chunk_id,
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

This evaluation-deep-dive note describes every chunk carries source, title, section,
chunk_id, offsets, and page information when available. The section is intentionally
verbose so that indexing tests have enough material to form realistic chunks. A
retrieval system should keep the relationship between the user question, the original
source, and the surrounding section visible. When a chunk crosses a boundary, the answer
may still be relevant, but the metadata becomes less precise for review and citation.
When a chunk is too small, it can lose setup, definitions, and examples that make the
result useful to a reader. The preferred implementation records offsets, stable
identifiers, and plain text so that a later answer can cite the exact file or page.
Topic marker 034 repeats the phrase chunk metadata to make evaluation queries
deterministic without hiding the normal prose around it.

## Section 03: Fixed Windows

This evaluation note describes fixed chunking uses bounded character windows with
overlap and whitespace-aware break points. The section is intentionally verbose so that
indexing tests have enough material to form realistic chunks. A retrieval system should
keep the relationship between the user question, the original source, and the
surrounding section visible. When a chunk crosses a boundary, the answer may still be
relevant, but the metadata becomes less precise for review and citation. When a chunk is
too small, it can lose setup, definitions, and examples that make the result useful to a
reader. The preferred implementation records offsets, stable identifiers, and plain text
so that a later answer can cite the exact file or page. Topic marker 003 repeats the
phrase fixed windows to make evaluation queries deterministic without hiding the normal
prose around it.

This evaluation-deep-dive note describes fixed chunking uses bounded character windows
with overlap and whitespace-aware break points. The section is intentionally verbose so
that indexing tests have enough material to form realistic chunks. A retrieval system
should keep the relationship between the user question, the original source, and the
surrounding section visible. When a chunk crosses a boundary, the answer may still be
relevant, but the metadata becomes less precise for review and citation. When a chunk is
too small, it can lose setup, definitions, and examples that make the result useful to a
reader. The preferred implementation records offsets, stable identifiers, and plain text
so that a later answer can cite the exact file or page. Topic marker 035 repeats the
phrase fixed windows to make evaluation queries deterministic without hiding the normal
prose around it.

## Section 04: Structural Boundaries

This evaluation note describes structural chunking starts from headings, pages, files,
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

This evaluation-deep-dive note describes structural chunking starts from headings,
pages, files, classes, and functions. The section is intentionally verbose so that
indexing tests have enough material to form realistic chunks. A retrieval system should
keep the relationship between the user question, the original source, and the
surrounding section visible. When a chunk crosses a boundary, the answer may still be
relevant, but the metadata becomes less precise for review and citation. When a chunk is
too small, it can lose setup, definitions, and examples that make the result useful to a
reader. The preferred implementation records offsets, stable identifiers, and plain text
so that a later answer can cite the exact file or page. Topic marker 036 repeats the
phrase structural boundaries to make evaluation queries deterministic without hiding the
normal prose around it.

## Section 05: Embedding Backend

This evaluation note describes Ollama embeddings are requested through the local HTTP
API and stored as normalized vectors. The section is intentionally verbose so that
indexing tests have enough material to form realistic chunks. A retrieval system should
keep the relationship between the user question, the original source, and the
surrounding section visible. When a chunk crosses a boundary, the answer may still be
relevant, but the metadata becomes less precise for review and citation. When a chunk is
too small, it can lose setup, definitions, and examples that make the result useful to a
reader. The preferred implementation records offsets, stable identifiers, and plain text
so that a later answer can cite the exact file or page. Topic marker 005 repeats the
phrase embedding backend to make evaluation queries deterministic without hiding the
normal prose around it.

This evaluation-deep-dive note describes Ollama embeddings are requested through the
local HTTP API and stored as normalized vectors. The section is intentionally verbose so
that indexing tests have enough material to form realistic chunks. A retrieval system
should keep the relationship between the user question, the original source, and the
surrounding section visible. When a chunk crosses a boundary, the answer may still be
relevant, but the metadata becomes less precise for review and citation. When a chunk is
too small, it can lose setup, definitions, and examples that make the result useful to a
reader. The preferred implementation records offsets, stable identifiers, and plain text
so that a later answer can cite the exact file or page. Topic marker 037 repeats the
phrase embedding backend to make evaluation queries deterministic without hiding the
normal prose around it.

## Section 06: Vector Storage

This evaluation note describes FAISS is used when installed and NumPy vectors remain
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

This evaluation-deep-dive note describes FAISS is used when installed and NumPy vectors
remain available as a portable fallback. The section is intentionally verbose so that
indexing tests have enough material to form realistic chunks. A retrieval system should
keep the relationship between the user question, the original source, and the
surrounding section visible. When a chunk crosses a boundary, the answer may still be
relevant, but the metadata becomes less precise for review and citation. When a chunk is
too small, it can lose setup, definitions, and examples that make the result useful to a
reader. The preferred implementation records offsets, stable identifiers, and plain text
so that a later answer can cite the exact file or page. Topic marker 038 repeats the
phrase vector storage to make evaluation queries deterministic without hiding the normal
prose around it.

## Section 07: Retrieval Metrics

This evaluation note describes comparison uses hit at k, reciprocal rank, source
accuracy, and section accuracy. The section is intentionally verbose so that indexing
tests have enough material to form realistic chunks. A retrieval system should keep the
relationship between the user question, the original source, and the surrounding section
visible. When a chunk crosses a boundary, the answer may still be relevant, but the
metadata becomes less precise for review and citation. When a chunk is too small, it can
lose setup, definitions, and examples that make the result useful to a reader. The
preferred implementation records offsets, stable identifiers, and plain text so that a
later answer can cite the exact file or page. Topic marker 007 repeats the phrase
retrieval metrics to make evaluation queries deterministic without hiding the normal
prose around it.

This evaluation-deep-dive note describes comparison uses hit at k, reciprocal rank,
source accuracy, and section accuracy. The section is intentionally verbose so that
indexing tests have enough material to form realistic chunks. A retrieval system should
keep the relationship between the user question, the original source, and the
surrounding section visible. When a chunk crosses a boundary, the answer may still be
relevant, but the metadata becomes less precise for review and citation. When a chunk is
too small, it can lose setup, definitions, and examples that make the result useful to a
reader. The preferred implementation records offsets, stable identifiers, and plain text
so that a later answer can cite the exact file or page. Topic marker 039 repeats the
phrase retrieval metrics to make evaluation queries deterministic without hiding the
normal prose around it.

## Section 08: Operational Checks

This evaluation note describes the pipeline verifies document count, estimated pages,
chunk counts, and metadata coverage. The section is intentionally verbose so that
indexing tests have enough material to form realistic chunks. A retrieval system should
keep the relationship between the user question, the original source, and the
surrounding section visible. When a chunk crosses a boundary, the answer may still be
relevant, but the metadata becomes less precise for review and citation. When a chunk is
too small, it can lose setup, definitions, and examples that make the result useful to a
reader. The preferred implementation records offsets, stable identifiers, and plain text
so that a later answer can cite the exact file or page. Topic marker 008 repeats the
phrase operational checks to make evaluation queries deterministic without hiding the
normal prose around it.

This evaluation-deep-dive note describes the pipeline verifies document count, estimated
pages, chunk counts, and metadata coverage. The section is intentionally verbose so that
indexing tests have enough material to form realistic chunks. A retrieval system should
keep the relationship between the user question, the original source, and the
surrounding section visible. When a chunk crosses a boundary, the answer may still be
relevant, but the metadata becomes less precise for review and citation. When a chunk is
too small, it can lose setup, definitions, and examples that make the result useful to a
reader. The preferred implementation records offsets, stable identifiers, and plain text
so that a later answer can cite the exact file or page. Topic marker 040 repeats the
phrase operational checks to make evaluation queries deterministic without hiding the
normal prose around it.

## Section 09: Ingestion Contract

This evaluation note describes loaders preserve source paths, document titles, page
numbers, and a stable kind field. The section is intentionally verbose so that indexing
tests have enough material to form realistic chunks. A retrieval system should keep the
relationship between the user question, the original source, and the surrounding section
visible. When a chunk crosses a boundary, the answer may still be relevant, but the
metadata becomes less precise for review and citation. When a chunk is too small, it can
lose setup, definitions, and examples that make the result useful to a reader. The
preferred implementation records offsets, stable identifiers, and plain text so that a
later answer can cite the exact file or page. Topic marker 009 repeats the phrase
ingestion contract to make evaluation queries deterministic without hiding the normal
prose around it.

This evaluation-deep-dive note describes loaders preserve source paths, document titles,
page numbers, and a stable kind field. The section is intentionally verbose so that
indexing tests have enough material to form realistic chunks. A retrieval system should
keep the relationship between the user question, the original source, and the
surrounding section visible. When a chunk crosses a boundary, the answer may still be
relevant, but the metadata becomes less precise for review and citation. When a chunk is
too small, it can lose setup, definitions, and examples that make the result useful to a
reader. The preferred implementation records offsets, stable identifiers, and plain text
so that a later answer can cite the exact file or page. Topic marker 041 repeats the
phrase ingestion contract to make evaluation queries deterministic without hiding the
normal prose around it.

## Section 10: Chunk Metadata

This evaluation note describes every chunk carries source, title, section, chunk_id,
offsets, and page information when available. The section is intentionally verbose so
that indexing tests have enough material to form realistic chunks. A retrieval system
should keep the relationship between the user question, the original source, and the
surrounding section visible. When a chunk crosses a boundary, the answer may still be
relevant, but the metadata becomes less precise for review and citation. When a chunk is
too small, it can lose setup, definitions, and examples that make the result useful to a
reader. The preferred implementation records offsets, stable identifiers, and plain text
so that a later answer can cite the exact file or page. Topic marker 010 repeats the
phrase chunk metadata to make evaluation queries deterministic without hiding the normal
prose around it.

This evaluation-deep-dive note describes every chunk carries source, title, section,
chunk_id, offsets, and page information when available. The section is intentionally
verbose so that indexing tests have enough material to form realistic chunks. A
retrieval system should keep the relationship between the user question, the original
source, and the surrounding section visible. When a chunk crosses a boundary, the answer
may still be relevant, but the metadata becomes less precise for review and citation.
When a chunk is too small, it can lose setup, definitions, and examples that make the
result useful to a reader. The preferred implementation records offsets, stable
identifiers, and plain text so that a later answer can cite the exact file or page.
Topic marker 042 repeats the phrase chunk metadata to make evaluation queries
deterministic without hiding the normal prose around it.

## Section 11: Fixed Windows

This evaluation note describes fixed chunking uses bounded character windows with
overlap and whitespace-aware break points. The section is intentionally verbose so that
indexing tests have enough material to form realistic chunks. A retrieval system should
keep the relationship between the user question, the original source, and the
surrounding section visible. When a chunk crosses a boundary, the answer may still be
relevant, but the metadata becomes less precise for review and citation. When a chunk is
too small, it can lose setup, definitions, and examples that make the result useful to a
reader. The preferred implementation records offsets, stable identifiers, and plain text
so that a later answer can cite the exact file or page. Topic marker 011 repeats the
phrase fixed windows to make evaluation queries deterministic without hiding the normal
prose around it.

This evaluation-deep-dive note describes fixed chunking uses bounded character windows
with overlap and whitespace-aware break points. The section is intentionally verbose so
that indexing tests have enough material to form realistic chunks. A retrieval system
should keep the relationship between the user question, the original source, and the
surrounding section visible. When a chunk crosses a boundary, the answer may still be
relevant, but the metadata becomes less precise for review and citation. When a chunk is
too small, it can lose setup, definitions, and examples that make the result useful to a
reader. The preferred implementation records offsets, stable identifiers, and plain text
so that a later answer can cite the exact file or page. Topic marker 043 repeats the
phrase fixed windows to make evaluation queries deterministic without hiding the normal
prose around it.

## Section 12: Structural Boundaries

This evaluation note describes structural chunking starts from headings, pages, files,
classes, and functions. The section is intentionally verbose so that indexing tests have
enough material to form realistic chunks. A retrieval system should keep the
relationship between the user question, the original source, and the surrounding section
visible. When a chunk crosses a boundary, the answer may still be relevant, but the
metadata becomes less precise for review and citation. When a chunk is too small, it can
lose setup, definitions, and examples that make the result useful to a reader. The
preferred implementation records offsets, stable identifiers, and plain text so that a
later answer can cite the exact file or page. Topic marker 012 repeats the phrase
structural boundaries to make evaluation queries deterministic without hiding the normal
prose around it.

This evaluation-deep-dive note describes structural chunking starts from headings,
pages, files, classes, and functions. The section is intentionally verbose so that
indexing tests have enough material to form realistic chunks. A retrieval system should
keep the relationship between the user question, the original source, and the
surrounding section visible. When a chunk crosses a boundary, the answer may still be
relevant, but the metadata becomes less precise for review and citation. When a chunk is
too small, it can lose setup, definitions, and examples that make the result useful to a
reader. The preferred implementation records offsets, stable identifiers, and plain text
so that a later answer can cite the exact file or page. Topic marker 044 repeats the
phrase structural boundaries to make evaluation queries deterministic without hiding the
normal prose around it.

## Section 13: Embedding Backend

This evaluation note describes Ollama embeddings are requested through the local HTTP
API and stored as normalized vectors. The section is intentionally verbose so that
indexing tests have enough material to form realistic chunks. A retrieval system should
keep the relationship between the user question, the original source, and the
surrounding section visible. When a chunk crosses a boundary, the answer may still be
relevant, but the metadata becomes less precise for review and citation. When a chunk is
too small, it can lose setup, definitions, and examples that make the result useful to a
reader. The preferred implementation records offsets, stable identifiers, and plain text
so that a later answer can cite the exact file or page. Topic marker 013 repeats the
phrase embedding backend to make evaluation queries deterministic without hiding the
normal prose around it.

This evaluation-deep-dive note describes Ollama embeddings are requested through the
local HTTP API and stored as normalized vectors. The section is intentionally verbose so
that indexing tests have enough material to form realistic chunks. A retrieval system
should keep the relationship between the user question, the original source, and the
surrounding section visible. When a chunk crosses a boundary, the answer may still be
relevant, but the metadata becomes less precise for review and citation. When a chunk is
too small, it can lose setup, definitions, and examples that make the result useful to a
reader. The preferred implementation records offsets, stable identifiers, and plain text
so that a later answer can cite the exact file or page. Topic marker 045 repeats the
phrase embedding backend to make evaluation queries deterministic without hiding the
normal prose around it.

## Section 14: Vector Storage

This evaluation note describes FAISS is used when installed and NumPy vectors remain
available as a portable fallback. The section is intentionally verbose so that indexing
tests have enough material to form realistic chunks. A retrieval system should keep the
relationship between the user question, the original source, and the surrounding section
visible. When a chunk crosses a boundary, the answer may still be relevant, but the
metadata becomes less precise for review and citation. When a chunk is too small, it can
lose setup, definitions, and examples that make the result useful to a reader. The
preferred implementation records offsets, stable identifiers, and plain text so that a
later answer can cite the exact file or page. Topic marker 014 repeats the phrase vector
storage to make evaluation queries deterministic without hiding the normal prose around
it.

This evaluation-deep-dive note describes FAISS is used when installed and NumPy vectors
remain available as a portable fallback. The section is intentionally verbose so that
indexing tests have enough material to form realistic chunks. A retrieval system should
keep the relationship between the user question, the original source, and the
surrounding section visible. When a chunk crosses a boundary, the answer may still be
relevant, but the metadata becomes less precise for review and citation. When a chunk is
too small, it can lose setup, definitions, and examples that make the result useful to a
reader. The preferred implementation records offsets, stable identifiers, and plain text
so that a later answer can cite the exact file or page. Topic marker 046 repeats the
phrase vector storage to make evaluation queries deterministic without hiding the normal
prose around it.

## Section 15: Retrieval Metrics

This evaluation note describes comparison uses hit at k, reciprocal rank, source
accuracy, and section accuracy. The section is intentionally verbose so that indexing
tests have enough material to form realistic chunks. A retrieval system should keep the
relationship between the user question, the original source, and the surrounding section
visible. When a chunk crosses a boundary, the answer may still be relevant, but the
metadata becomes less precise for review and citation. When a chunk is too small, it can
lose setup, definitions, and examples that make the result useful to a reader. The
preferred implementation records offsets, stable identifiers, and plain text so that a
later answer can cite the exact file or page. Topic marker 015 repeats the phrase
retrieval metrics to make evaluation queries deterministic without hiding the normal
prose around it.

This evaluation-deep-dive note describes comparison uses hit at k, reciprocal rank,
source accuracy, and section accuracy. The section is intentionally verbose so that
indexing tests have enough material to form realistic chunks. A retrieval system should
keep the relationship between the user question, the original source, and the
surrounding section visible. When a chunk crosses a boundary, the answer may still be
relevant, but the metadata becomes less precise for review and citation. When a chunk is
too small, it can lose setup, definitions, and examples that make the result useful to a
reader. The preferred implementation records offsets, stable identifiers, and plain text
so that a later answer can cite the exact file or page. Topic marker 047 repeats the
phrase retrieval metrics to make evaluation queries deterministic without hiding the
normal prose around it.

## Section 16: Operational Checks

This evaluation note describes the pipeline verifies document count, estimated pages,
chunk counts, and metadata coverage. The section is intentionally verbose so that
indexing tests have enough material to form realistic chunks. A retrieval system should
keep the relationship between the user question, the original source, and the
surrounding section visible. When a chunk crosses a boundary, the answer may still be
relevant, but the metadata becomes less precise for review and citation. When a chunk is
too small, it can lose setup, definitions, and examples that make the result useful to a
reader. The preferred implementation records offsets, stable identifiers, and plain text
so that a later answer can cite the exact file or page. Topic marker 016 repeats the
phrase operational checks to make evaluation queries deterministic without hiding the
normal prose around it.

This evaluation-deep-dive note describes the pipeline verifies document count, estimated
pages, chunk counts, and metadata coverage. The section is intentionally verbose so that
indexing tests have enough material to form realistic chunks. A retrieval system should
keep the relationship between the user question, the original source, and the
surrounding section visible. When a chunk crosses a boundary, the answer may still be
relevant, but the metadata becomes less precise for review and citation. When a chunk is
too small, it can lose setup, definitions, and examples that make the result useful to a
reader. The preferred implementation records offsets, stable identifiers, and plain text
so that a later answer can cite the exact file or page. Topic marker 048 repeats the
phrase operational checks to make evaluation queries deterministic without hiding the
normal prose around it.

## Section 17: Ingestion Contract

This evaluation note describes loaders preserve source paths, document titles, page
numbers, and a stable kind field. The section is intentionally verbose so that indexing
tests have enough material to form realistic chunks. A retrieval system should keep the
relationship between the user question, the original source, and the surrounding section
visible. When a chunk crosses a boundary, the answer may still be relevant, but the
metadata becomes less precise for review and citation. When a chunk is too small, it can
lose setup, definitions, and examples that make the result useful to a reader. The
preferred implementation records offsets, stable identifiers, and plain text so that a
later answer can cite the exact file or page. Topic marker 017 repeats the phrase
ingestion contract to make evaluation queries deterministic without hiding the normal
prose around it.

This evaluation-deep-dive note describes loaders preserve source paths, document titles,
page numbers, and a stable kind field. The section is intentionally verbose so that
indexing tests have enough material to form realistic chunks. A retrieval system should
keep the relationship between the user question, the original source, and the
surrounding section visible. When a chunk crosses a boundary, the answer may still be
relevant, but the metadata becomes less precise for review and citation. When a chunk is
too small, it can lose setup, definitions, and examples that make the result useful to a
reader. The preferred implementation records offsets, stable identifiers, and plain text
so that a later answer can cite the exact file or page. Topic marker 049 repeats the
phrase ingestion contract to make evaluation queries deterministic without hiding the
normal prose around it.

## Section 18: Chunk Metadata

This evaluation note describes every chunk carries source, title, section, chunk_id,
offsets, and page information when available. The section is intentionally verbose so
that indexing tests have enough material to form realistic chunks. A retrieval system
should keep the relationship between the user question, the original source, and the
surrounding section visible. When a chunk crosses a boundary, the answer may still be
relevant, but the metadata becomes less precise for review and citation. When a chunk is
too small, it can lose setup, definitions, and examples that make the result useful to a
reader. The preferred implementation records offsets, stable identifiers, and plain text
so that a later answer can cite the exact file or page. Topic marker 018 repeats the
phrase chunk metadata to make evaluation queries deterministic without hiding the normal
prose around it.

This evaluation-deep-dive note describes every chunk carries source, title, section,
chunk_id, offsets, and page information when available. The section is intentionally
verbose so that indexing tests have enough material to form realistic chunks. A
retrieval system should keep the relationship between the user question, the original
source, and the surrounding section visible. When a chunk crosses a boundary, the answer
may still be relevant, but the metadata becomes less precise for review and citation.
When a chunk is too small, it can lose setup, definitions, and examples that make the
result useful to a reader. The preferred implementation records offsets, stable
identifiers, and plain text so that a later answer can cite the exact file or page.
Topic marker 050 repeats the phrase chunk metadata to make evaluation queries
deterministic without hiding the normal prose around it.

## Section 19: Fixed Windows

This evaluation note describes fixed chunking uses bounded character windows with
overlap and whitespace-aware break points. The section is intentionally verbose so that
indexing tests have enough material to form realistic chunks. A retrieval system should
keep the relationship between the user question, the original source, and the
surrounding section visible. When a chunk crosses a boundary, the answer may still be
relevant, but the metadata becomes less precise for review and citation. When a chunk is
too small, it can lose setup, definitions, and examples that make the result useful to a
reader. The preferred implementation records offsets, stable identifiers, and plain text
so that a later answer can cite the exact file or page. Topic marker 019 repeats the
phrase fixed windows to make evaluation queries deterministic without hiding the normal
prose around it.

This evaluation-deep-dive note describes fixed chunking uses bounded character windows
with overlap and whitespace-aware break points. The section is intentionally verbose so
that indexing tests have enough material to form realistic chunks. A retrieval system
should keep the relationship between the user question, the original source, and the
surrounding section visible. When a chunk crosses a boundary, the answer may still be
relevant, but the metadata becomes less precise for review and citation. When a chunk is
too small, it can lose setup, definitions, and examples that make the result useful to a
reader. The preferred implementation records offsets, stable identifiers, and plain text
so that a later answer can cite the exact file or page. Topic marker 051 repeats the
phrase fixed windows to make evaluation queries deterministic without hiding the normal
prose around it.

## Section 20: Structural Boundaries

This evaluation note describes structural chunking starts from headings, pages, files,
classes, and functions. The section is intentionally verbose so that indexing tests have
enough material to form realistic chunks. A retrieval system should keep the
relationship between the user question, the original source, and the surrounding section
visible. When a chunk crosses a boundary, the answer may still be relevant, but the
metadata becomes less precise for review and citation. When a chunk is too small, it can
lose setup, definitions, and examples that make the result useful to a reader. The
preferred implementation records offsets, stable identifiers, and plain text so that a
later answer can cite the exact file or page. Topic marker 020 repeats the phrase
structural boundaries to make evaluation queries deterministic without hiding the normal
prose around it.

This evaluation-deep-dive note describes structural chunking starts from headings,
pages, files, classes, and functions. The section is intentionally verbose so that
indexing tests have enough material to form realistic chunks. A retrieval system should
keep the relationship between the user question, the original source, and the
surrounding section visible. When a chunk crosses a boundary, the answer may still be
relevant, but the metadata becomes less precise for review and citation. When a chunk is
too small, it can lose setup, definitions, and examples that make the result useful to a
reader. The preferred implementation records offsets, stable identifiers, and plain text
so that a later answer can cite the exact file or page. Topic marker 052 repeats the
phrase structural boundaries to make evaluation queries deterministic without hiding the
normal prose around it.

## Section 21: Embedding Backend

This evaluation note describes Ollama embeddings are requested through the local HTTP
API and stored as normalized vectors. The section is intentionally verbose so that
indexing tests have enough material to form realistic chunks. A retrieval system should
keep the relationship between the user question, the original source, and the
surrounding section visible. When a chunk crosses a boundary, the answer may still be
relevant, but the metadata becomes less precise for review and citation. When a chunk is
too small, it can lose setup, definitions, and examples that make the result useful to a
reader. The preferred implementation records offsets, stable identifiers, and plain text
so that a later answer can cite the exact file or page. Topic marker 021 repeats the
phrase embedding backend to make evaluation queries deterministic without hiding the
normal prose around it.

This evaluation-deep-dive note describes Ollama embeddings are requested through the
local HTTP API and stored as normalized vectors. The section is intentionally verbose so
that indexing tests have enough material to form realistic chunks. A retrieval system
should keep the relationship between the user question, the original source, and the
surrounding section visible. When a chunk crosses a boundary, the answer may still be
relevant, but the metadata becomes less precise for review and citation. When a chunk is
too small, it can lose setup, definitions, and examples that make the result useful to a
reader. The preferred implementation records offsets, stable identifiers, and plain text
so that a later answer can cite the exact file or page. Topic marker 053 repeats the
phrase embedding backend to make evaluation queries deterministic without hiding the
normal prose around it.

## Section 22: Vector Storage

This evaluation note describes FAISS is used when installed and NumPy vectors remain
available as a portable fallback. The section is intentionally verbose so that indexing
tests have enough material to form realistic chunks. A retrieval system should keep the
relationship between the user question, the original source, and the surrounding section
visible. When a chunk crosses a boundary, the answer may still be relevant, but the
metadata becomes less precise for review and citation. When a chunk is too small, it can
lose setup, definitions, and examples that make the result useful to a reader. The
preferred implementation records offsets, stable identifiers, and plain text so that a
later answer can cite the exact file or page. Topic marker 022 repeats the phrase vector
storage to make evaluation queries deterministic without hiding the normal prose around
it.

This evaluation-deep-dive note describes FAISS is used when installed and NumPy vectors
remain available as a portable fallback. The section is intentionally verbose so that
indexing tests have enough material to form realistic chunks. A retrieval system should
keep the relationship between the user question, the original source, and the
surrounding section visible. When a chunk crosses a boundary, the answer may still be
relevant, but the metadata becomes less precise for review and citation. When a chunk is
too small, it can lose setup, definitions, and examples that make the result useful to a
reader. The preferred implementation records offsets, stable identifiers, and plain text
so that a later answer can cite the exact file or page. Topic marker 054 repeats the
phrase vector storage to make evaluation queries deterministic without hiding the normal
prose around it.

## Section 23: Retrieval Metrics

This evaluation note describes comparison uses hit at k, reciprocal rank, source
accuracy, and section accuracy. The section is intentionally verbose so that indexing
tests have enough material to form realistic chunks. A retrieval system should keep the
relationship between the user question, the original source, and the surrounding section
visible. When a chunk crosses a boundary, the answer may still be relevant, but the
metadata becomes less precise for review and citation. When a chunk is too small, it can
lose setup, definitions, and examples that make the result useful to a reader. The
preferred implementation records offsets, stable identifiers, and plain text so that a
later answer can cite the exact file or page. Topic marker 023 repeats the phrase
retrieval metrics to make evaluation queries deterministic without hiding the normal
prose around it.

This evaluation-deep-dive note describes comparison uses hit at k, reciprocal rank,
source accuracy, and section accuracy. The section is intentionally verbose so that
indexing tests have enough material to form realistic chunks. A retrieval system should
keep the relationship between the user question, the original source, and the
surrounding section visible. When a chunk crosses a boundary, the answer may still be
relevant, but the metadata becomes less precise for review and citation. When a chunk is
too small, it can lose setup, definitions, and examples that make the result useful to a
reader. The preferred implementation records offsets, stable identifiers, and plain text
so that a later answer can cite the exact file or page. Topic marker 055 repeats the
phrase retrieval metrics to make evaluation queries deterministic without hiding the
normal prose around it.

## Section 24: Operational Checks

This evaluation note describes the pipeline verifies document count, estimated pages,
chunk counts, and metadata coverage. The section is intentionally verbose so that
indexing tests have enough material to form realistic chunks. A retrieval system should
keep the relationship between the user question, the original source, and the
surrounding section visible. When a chunk crosses a boundary, the answer may still be
relevant, but the metadata becomes less precise for review and citation. When a chunk is
too small, it can lose setup, definitions, and examples that make the result useful to a
reader. The preferred implementation records offsets, stable identifiers, and plain text
so that a later answer can cite the exact file or page. Topic marker 024 repeats the
phrase operational checks to make evaluation queries deterministic without hiding the
normal prose around it.

This evaluation-deep-dive note describes the pipeline verifies document count, estimated
pages, chunk counts, and metadata coverage. The section is intentionally verbose so that
indexing tests have enough material to form realistic chunks. A retrieval system should
keep the relationship between the user question, the original source, and the
surrounding section visible. When a chunk crosses a boundary, the answer may still be
relevant, but the metadata becomes less precise for review and citation. When a chunk is
too small, it can lose setup, definitions, and examples that make the result useful to a
reader. The preferred implementation records offsets, stable identifiers, and plain text
so that a later answer can cite the exact file or page. Topic marker 056 repeats the
phrase operational checks to make evaluation queries deterministic without hiding the
normal prose around it.

## Section 25: Ingestion Contract

This evaluation note describes loaders preserve source paths, document titles, page
numbers, and a stable kind field. The section is intentionally verbose so that indexing
tests have enough material to form realistic chunks. A retrieval system should keep the
relationship between the user question, the original source, and the surrounding section
visible. When a chunk crosses a boundary, the answer may still be relevant, but the
metadata becomes less precise for review and citation. When a chunk is too small, it can
lose setup, definitions, and examples that make the result useful to a reader. The
preferred implementation records offsets, stable identifiers, and plain text so that a
later answer can cite the exact file or page. Topic marker 025 repeats the phrase
ingestion contract to make evaluation queries deterministic without hiding the normal
prose around it.

This evaluation-deep-dive note describes loaders preserve source paths, document titles,
page numbers, and a stable kind field. The section is intentionally verbose so that
indexing tests have enough material to form realistic chunks. A retrieval system should
keep the relationship between the user question, the original source, and the
surrounding section visible. When a chunk crosses a boundary, the answer may still be
relevant, but the metadata becomes less precise for review and citation. When a chunk is
too small, it can lose setup, definitions, and examples that make the result useful to a
reader. The preferred implementation records offsets, stable identifiers, and plain text
so that a later answer can cite the exact file or page. Topic marker 057 repeats the
phrase ingestion contract to make evaluation queries deterministic without hiding the
normal prose around it.

## Section 26: Chunk Metadata

This evaluation note describes every chunk carries source, title, section, chunk_id,
offsets, and page information when available. The section is intentionally verbose so
that indexing tests have enough material to form realistic chunks. A retrieval system
should keep the relationship between the user question, the original source, and the
surrounding section visible. When a chunk crosses a boundary, the answer may still be
relevant, but the metadata becomes less precise for review and citation. When a chunk is
too small, it can lose setup, definitions, and examples that make the result useful to a
reader. The preferred implementation records offsets, stable identifiers, and plain text
so that a later answer can cite the exact file or page. Topic marker 026 repeats the
phrase chunk metadata to make evaluation queries deterministic without hiding the normal
prose around it.

This evaluation-deep-dive note describes every chunk carries source, title, section,
chunk_id, offsets, and page information when available. The section is intentionally
verbose so that indexing tests have enough material to form realistic chunks. A
retrieval system should keep the relationship between the user question, the original
source, and the surrounding section visible. When a chunk crosses a boundary, the answer
may still be relevant, but the metadata becomes less precise for review and citation.
When a chunk is too small, it can lose setup, definitions, and examples that make the
result useful to a reader. The preferred implementation records offsets, stable
identifiers, and plain text so that a later answer can cite the exact file or page.
Topic marker 058 repeats the phrase chunk metadata to make evaluation queries
deterministic without hiding the normal prose around it.

## Section 27: Fixed Windows

This evaluation note describes fixed chunking uses bounded character windows with
overlap and whitespace-aware break points. The section is intentionally verbose so that
indexing tests have enough material to form realistic chunks. A retrieval system should
keep the relationship between the user question, the original source, and the
surrounding section visible. When a chunk crosses a boundary, the answer may still be
relevant, but the metadata becomes less precise for review and citation. When a chunk is
too small, it can lose setup, definitions, and examples that make the result useful to a
reader. The preferred implementation records offsets, stable identifiers, and plain text
so that a later answer can cite the exact file or page. Topic marker 027 repeats the
phrase fixed windows to make evaluation queries deterministic without hiding the normal
prose around it.

This evaluation-deep-dive note describes fixed chunking uses bounded character windows
with overlap and whitespace-aware break points. The section is intentionally verbose so
that indexing tests have enough material to form realistic chunks. A retrieval system
should keep the relationship between the user question, the original source, and the
surrounding section visible. When a chunk crosses a boundary, the answer may still be
relevant, but the metadata becomes less precise for review and citation. When a chunk is
too small, it can lose setup, definitions, and examples that make the result useful to a
reader. The preferred implementation records offsets, stable identifiers, and plain text
so that a later answer can cite the exact file or page. Topic marker 059 repeats the
phrase fixed windows to make evaluation queries deterministic without hiding the normal
prose around it.

## Section 28: Structural Boundaries

This evaluation note describes structural chunking starts from headings, pages, files,
classes, and functions. The section is intentionally verbose so that indexing tests have
enough material to form realistic chunks. A retrieval system should keep the
relationship between the user question, the original source, and the surrounding section
visible. When a chunk crosses a boundary, the answer may still be relevant, but the
metadata becomes less precise for review and citation. When a chunk is too small, it can
lose setup, definitions, and examples that make the result useful to a reader. The
preferred implementation records offsets, stable identifiers, and plain text so that a
later answer can cite the exact file or page. Topic marker 028 repeats the phrase
structural boundaries to make evaluation queries deterministic without hiding the normal
prose around it.

This evaluation-deep-dive note describes structural chunking starts from headings,
pages, files, classes, and functions. The section is intentionally verbose so that
indexing tests have enough material to form realistic chunks. A retrieval system should
keep the relationship between the user question, the original source, and the
surrounding section visible. When a chunk crosses a boundary, the answer may still be
relevant, but the metadata becomes less precise for review and citation. When a chunk is
too small, it can lose setup, definitions, and examples that make the result useful to a
reader. The preferred implementation records offsets, stable identifiers, and plain text
so that a later answer can cite the exact file or page. Topic marker 060 repeats the
phrase structural boundaries to make evaluation queries deterministic without hiding the
normal prose around it.

## Section 29: Embedding Backend

This evaluation note describes Ollama embeddings are requested through the local HTTP
API and stored as normalized vectors. The section is intentionally verbose so that
indexing tests have enough material to form realistic chunks. A retrieval system should
keep the relationship between the user question, the original source, and the
surrounding section visible. When a chunk crosses a boundary, the answer may still be
relevant, but the metadata becomes less precise for review and citation. When a chunk is
too small, it can lose setup, definitions, and examples that make the result useful to a
reader. The preferred implementation records offsets, stable identifiers, and plain text
so that a later answer can cite the exact file or page. Topic marker 029 repeats the
phrase embedding backend to make evaluation queries deterministic without hiding the
normal prose around it.

This evaluation-deep-dive note describes Ollama embeddings are requested through the
local HTTP API and stored as normalized vectors. The section is intentionally verbose so
that indexing tests have enough material to form realistic chunks. A retrieval system
should keep the relationship between the user question, the original source, and the
surrounding section visible. When a chunk crosses a boundary, the answer may still be
relevant, but the metadata becomes less precise for review and citation. When a chunk is
too small, it can lose setup, definitions, and examples that make the result useful to a
reader. The preferred implementation records offsets, stable identifiers, and plain text
so that a later answer can cite the exact file or page. Topic marker 061 repeats the
phrase embedding backend to make evaluation queries deterministic without hiding the
normal prose around it.

## Section 30: Vector Storage

This evaluation note describes FAISS is used when installed and NumPy vectors remain
available as a portable fallback. The section is intentionally verbose so that indexing
tests have enough material to form realistic chunks. A retrieval system should keep the
relationship between the user question, the original source, and the surrounding section
visible. When a chunk crosses a boundary, the answer may still be relevant, but the
metadata becomes less precise for review and citation. When a chunk is too small, it can
lose setup, definitions, and examples that make the result useful to a reader. The
preferred implementation records offsets, stable identifiers, and plain text so that a
later answer can cite the exact file or page. Topic marker 030 repeats the phrase vector
storage to make evaluation queries deterministic without hiding the normal prose around
it.

This evaluation-deep-dive note describes FAISS is used when installed and NumPy vectors
remain available as a portable fallback. The section is intentionally verbose so that
indexing tests have enough material to form realistic chunks. A retrieval system should
keep the relationship between the user question, the original source, and the
surrounding section visible. When a chunk crosses a boundary, the answer may still be
relevant, but the metadata becomes less precise for review and citation. When a chunk is
too small, it can lose setup, definitions, and examples that make the result useful to a
reader. The preferred implementation records offsets, stable identifiers, and plain text
so that a later answer can cite the exact file or page. Topic marker 062 repeats the
phrase vector storage to make evaluation queries deterministic without hiding the normal
prose around it.

## Section 31: Retrieval Metrics

This evaluation note describes comparison uses hit at k, reciprocal rank, source
accuracy, and section accuracy. The section is intentionally verbose so that indexing
tests have enough material to form realistic chunks. A retrieval system should keep the
relationship between the user question, the original source, and the surrounding section
visible. When a chunk crosses a boundary, the answer may still be relevant, but the
metadata becomes less precise for review and citation. When a chunk is too small, it can
lose setup, definitions, and examples that make the result useful to a reader. The
preferred implementation records offsets, stable identifiers, and plain text so that a
later answer can cite the exact file or page. Topic marker 031 repeats the phrase
retrieval metrics to make evaluation queries deterministic without hiding the normal
prose around it.

This evaluation-deep-dive note describes comparison uses hit at k, reciprocal rank,
source accuracy, and section accuracy. The section is intentionally verbose so that
indexing tests have enough material to form realistic chunks. A retrieval system should
keep the relationship between the user question, the original source, and the
surrounding section visible. When a chunk crosses a boundary, the answer may still be
relevant, but the metadata becomes less precise for review and citation. When a chunk is
too small, it can lose setup, definitions, and examples that make the result useful to a
reader. The preferred implementation records offsets, stable identifiers, and plain text
so that a later answer can cite the exact file or page. Topic marker 063 repeats the
phrase retrieval metrics to make evaluation queries deterministic without hiding the
normal prose around it.

## Section 32: Operational Checks

This evaluation note describes the pipeline verifies document count, estimated pages,
chunk counts, and metadata coverage. The section is intentionally verbose so that
indexing tests have enough material to form realistic chunks. A retrieval system should
keep the relationship between the user question, the original source, and the
surrounding section visible. When a chunk crosses a boundary, the answer may still be
relevant, but the metadata becomes less precise for review and citation. When a chunk is
too small, it can lose setup, definitions, and examples that make the result useful to a
reader. The preferred implementation records offsets, stable identifiers, and plain text
so that a later answer can cite the exact file or page. Topic marker 032 repeats the
phrase operational checks to make evaluation queries deterministic without hiding the
normal prose around it.

This evaluation-deep-dive note describes the pipeline verifies document count, estimated
pages, chunk counts, and metadata coverage. The section is intentionally verbose so that
indexing tests have enough material to form realistic chunks. A retrieval system should
keep the relationship between the user question, the original source, and the
surrounding section visible. When a chunk crosses a boundary, the answer may still be
relevant, but the metadata becomes less precise for review and citation. When a chunk is
too small, it can lose setup, definitions, and examples that make the result useful to a
reader. The preferred implementation records offsets, stable identifiers, and plain text
so that a later answer can cite the exact file or page. Topic marker 064 repeats the
phrase operational checks to make evaluation queries deterministic without hiding the
normal prose around it.

