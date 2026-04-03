# Runbook: One-shot 9-book audit and publish

## 1) Rebuild notes and masters

```bash
python3 skills/book-audit/scripts/rebuild_notes_no_personal.py
```

## 2) Validate coverage quickly

```bash
python3 skills/book-audit/scripts/audit_books.py
```

## 3) Verify no personal context in notes

Search terms example:
- 阿山
- 吉众
- 祺富

## 4) Prepare GitHub export set

Include:
- `kb/books-notes/*/master.md`
- `kb/books-notes/*/slice_*_n.md`
- `kb/books-notes/*/meta.json`
- `kb/books-notes/QA-九本书复核报告.md`
- `skills/book-learner/**`
- `skills/book-audit/**`
- `skills/book-notes-sop/**`

Exclude:
- `kb/books-source/**`
- raw `slice_*.md` (without `_n`)

## 5) Commit and push

Commit message suggestion:
- `book-notes: full 9-book re-audit + neutralized notes + SOP skills`
