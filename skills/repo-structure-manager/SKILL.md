---
name: repo-structure-manager
description: Manage and normalize this GitHub skills repository layout. Use when reorganizing folders, merging duplicate skills, moving files to correct directories, deleting stale artifacts, updating indexes, and enforcing publish rules.
---

# Repo Structure Manager

Use this skill to keep the repository clean, consistent, and publish-ready.

## Target layout

- `skills/<skill-name>/` — all skill packages
- `README.md` + `REPO-INDEX.md` — repository navigation
- `.gitignore` — publication guardrails

Runtime outputs (logs, generated notes, datasets) should stay outside this repo.

## Mandatory checks

1. No skill folder at repository root except `skills/`.
2. Each skill folder must contain `SKILL.md`.
3. Remove stale backups (`*.bak*`, temp files) unless explicitly required.
4. Keep runtime data out of this repository.
5. Prevent source leakage (raw proprietary files, temporary extracts, local caches).

## Merge/cleanup strategy

1. Detect overlapping skills by scope and trigger phrases.
2. Keep one canonical skill; migrate useful references/scripts.
3. Delete deprecated duplicates after migration.
4. Update `README.md` and `REPO-INDEX.md` to reflect final structure.

## Deliverables per cleanup run

- Updated tree structure
- Added/updated index docs
- Created/updated management skill files
- Clean git diff (no unintended data leaks)
