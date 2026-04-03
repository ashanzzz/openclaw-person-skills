---
name: book-notes-sop
description: End-to-end SOP for large-scale book-note projects (multi-book re-audit, note normalization, skills refinement, and GitHub publishing). Use when user asks for one-shot unattended execution of complex book tasks with retries and final delivery without repeated prompting.
---

# Book Notes SOP

Execute this SOP for unattended, large book-processing tasks.

## Goal

Produce a clean, publishable knowledge package from local book data:
- Complete notes for all slices
- Strong master synthesis per book
- Skillized workflow for reuse
- GitHub push with notes + skills only

## Execution phases

1. **Baseline audit**
   - Count slices vs note slices per book
   - Identify missing notes and structural gaps

2. **Normalize notes**
   - Regenerate or repair missing/inconsistent `slice_XXX_n.md`
   - Enforce neutral style (no user-specific personal context)

3. **Strengthen master notes**
   - Ensure each `master.md` includes:
     - one-line thesis
     - core framework
     - chapter map
     - reusable SOP
     - common pitfalls

4. **Skill hardening**
   - Update `book-learner` and `book-audit`
   - Keep frontmatter minimal (`name`, `description` only)
   - Reference deterministic scripts for repeatability

5. **Publish gating**
   - Exclude EPUB and raw slices from commit
   - Include notes and skill assets only
   - Commit with audit report and push

## Hard constraints

- Do not publish:
  - `kb/books-source/*.epub`
  - raw `slice_XXX.md`
- Publish only:
  - `master.md`
  - `slice_XXX_n.md`
  - `meta.json`
  - audit reports
  - skill files (`skills/book-*/`)

## Retry discipline (unattended)

- On recoverable errors (timeout/IO/intermittent failure), auto-retry up to 3 times.
- Persist progress after each book to avoid losing work.
- If interrupted, resume from current filesystem state and continue to completion.
