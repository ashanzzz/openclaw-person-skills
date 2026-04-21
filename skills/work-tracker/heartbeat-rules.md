# Heartbeat Rules

Use heartbeat to keep `~/work-tracker/` organized and Vikunja state current.

## Source of Truth

Keep the workspace `HEARTBEAT.md` snippet minimal.
Treat this file as the stable contract for work-tracker heartbeat behavior.
Store mutable run state only in `~/work-tracker/heartbeat-state.md`.

## Start of Every Heartbeat

1. Ensure `~/work-tracker/heartbeat-state.md` exists.
2. Write `last_heartbeat_started_at` immediately in ISO 8601 (Beijing time).
3. Query Vikunja `/tasks` for current state.
4. Load `~/work-tracker/work-queue.md` for last snapshot.
5. Compare: new tasks, done changes, overdue items.

## If Nothing Material Changed

- Set `last_heartbeat_result: HEARTBEAT_OK`
- Append "no material change" note to last_actions
- Return `HEARTBEAT_OK`

## If Something Changed

Only do conservative updates:

- Update `work-queue.md` snapshot with new state
- Log any new completions to `completions.md`
- Log overdue items if they newly became overdue
- Check pending follow-ups if any parent task was completed
- Update `index.md` if counts drift

## Safety Rules

- Most heartbeat runs should do nothing visible
- Prefer append/snapshot over rewrite
- Never delete historical completion records
- Never mark a task done without explicit user signal
- If Vikunja unreachable: use last snapshot, mark `last_heartbeat_result: STALE`
- Never reorganize files outside `~/work-tracker/`
- If scope is ambiguous, leave files untouched

## Proactive Nudge on Heartbeat

If overdue task found and no nudge sent in 24h:
- Flag for user notification
- Update `last_nudge_at` in heartbeat-state

## State Fields

Keep `~/work-tracker/heartbeat-state.md` simple:

- `last_heartbeat_started_at`
- `last_reviewed_change_at`
- `last_heartbeat_result`
- `last_nudge_at`
- `last_actions`
