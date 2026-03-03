# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

## Local Search

- SearXNG: `http://192.168.8.11:6001`
- Scope: LAN only
- Notes: User authorized agent to adjust SearXNG settings as needed for research workflow.

### Multi-Channel Search (Default Hard Rule)

For all search/research/job-hunt tasks, run channels in parallel by default:
1. `SearXNG` (local first)
2. `web_search` API (configured skill/API channel)
3. `browser` live verification (open + click into details)

Execution rule:
- Do not rely on a single source when multiple channels are available.
- Merge results, dedupe, and mark source provenance.
- If one channel fails, continue with remaining channels and label gaps.

## Data Stores (user-confirmed)

- Qdrant
  - Endpoint: `http://192.168.8.11:6333`
- PostgreSQL (pgvector)
  - Host: `192.168.8.19`
  - Port: `5432`
  - Database: `openclaw`
  - Username: `openclaw`
  - Password: `openclaw`

---

Add whatever helps you do your job. This is your cheat sheet.

## ClawHub CLI (official)

- Official CLI command: `clawhub` (not `clawdhub`)
- Official docs: `/app/docs/tools/clawhub.md`
- Common commands:
  - `clawhub search "query"`
  - `clawhub install <skill-slug>`
  - `clawhub update --all`
