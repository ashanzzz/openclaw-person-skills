# Multi-Channel Search Playbook (Default)

## Channels
- A: Local SearXNG (`http://192.168.8.11:6001`)
- B: `web_search` API
- C: `browser` live page verification

## Flow
1. Run A+B in parallel to expand candidate coverage.
2. Use C to verify critical fields (official job URL, apply URL, posted date, requirements).
3. Merge + dedupe by `(company, title, official_job_url)`.
4. Save source tags: `searxng|api|browser|mixed`.

## Failure handling
- A fail: continue B+C
- B fail: continue A+C
- C fail: keep A+B results but force `verify_needed`

## Output quality gate
- Any item without browser-level detail verification cannot enter `apply_now`.
