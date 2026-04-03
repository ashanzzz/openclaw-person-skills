---
name: book-learner
description: Read and structure books from local EPUB/slice sources into reusable notes. Use when user asks to read a book, extract chapter notes, complete missing slice notes, or consolidate book content into master notes under kb/books-notes/<book>/.
---

# Book Learner

Use this skill to turn raw book content into stable note artifacts.

## Workflow

1. Identify source files (`kb/books-source/*.epub` and/or existing `slice_XXX.md`).
2. Ensure target folder exists at `kb/books-notes/<书名>/`.
3. For each `slice_XXX.md`, create/update `slice_XXX_n.md`.
4. Build/update `master.md` as the book-level synthesis.
5. Update `meta.json` status and slice counts.

## Required output per book

- `master.md` (book-level synthesis)
- `meta.json` (status/counts/ids)
- `slice_XXX_n.md` for every `slice_XXX.md`

## Local helper scripts

- `scripts/split_and_read.py` — inspect EPUB structure and slices
- `scripts/merge_slices.py` — merge local slices into one local `.md` (for reading only)
- `scripts/convert_epubs.py` — convert EPUB to local `.md` where structure allows

## Quality gates

- Note coverage: `count(slice_XXX_n.md) == count(slice_XXX.md)`
- Neutrality: notes must not include user-specific personal context
- Traceability: master sections must map back to chapter/slice evidence

## Publishing rule

- Do **not** publish EPUB files.
- Do **not** publish raw `slice_XXX.md`.
- Publish notes only: `master.md`, `slice_XXX_n.md`, `meta.json`, and skill files.
