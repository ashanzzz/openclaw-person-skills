# Heartbeat State — Template

Baseline for `~/work-tracker/heartbeat-state.md`.

```markdown
# Work Tracker Heartbeat State

last_heartbeat_started_at: never
last_reviewed_change_at: never
last_heartbeat_result: never
last_nudge_at: never

## Last actions
- none yet
```

## Field Meanings

- `last_heartbeat_started_at`: ISO 8601 Beijing time when heartbeat began
- `last_reviewed_change_at`: ISO 8601 Beijing time when changes were reviewed
- `last_heartbeat_result`: HEARTBEAT_OK | STALE | CHANGES_DETECTED | ERROR
- `last_nudge_at`: ISO 8601 Beijing time of last proactive nudge sent
- `last_actions`: brief log of what heartbeat did
