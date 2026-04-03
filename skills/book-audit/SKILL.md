---
name: book-audit
description: Audit and repair book-note integrity for kb/books-notes. Use when user asks to re-check reading status, verify slice-note matching, remove personal content from notes, or rebuild notes to a consistent SOP quality level.
---

# Book Audit

Use this skill to verify and normalize note quality across books.

## Core checks

1. **Coverage check**: every `slice_XXX.md` has corresponding `slice_XXX_n.md`.
2. **Status check**: `meta.json` reflects actual counts and completion state.
3. **Neutrality check**: notes contain no user-specific personal context.
4. **Master check**: `master.md` exists and includes framework + SOP + pitfalls.
5. **Publishability check**: repo commit excludes EPUB and raw slices.

## Scripts

- `scripts/audit_books.py` — tabular audit of completion and consistency
- `scripts/rebuild_notes_no_personal.py` — regenerate all slice notes + master notes in neutral style and produce QA report

## Standard run order

1. Run `audit_books.py` to establish baseline.
2. Run `rebuild_notes_no_personal.py` to repair and standardize.
3. Re-run `audit_books.py` to confirm 100% coverage.
4. Export notes + skills only to GitHub.

## Deliverables

- `kb/books-notes/QA-九本书复核报告.md`
- Updated per-book `master.md`
- Full `slice_XXX_n.md` coverage
- Updated skill SOP files
