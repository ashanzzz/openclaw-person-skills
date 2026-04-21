# Anticipations — What You Might Need — Template

Append to `~/work-tracker/anticipations.md`.

```markdown
# Anticipations — What You Might Need

## Needs (expressed 3x+, confirmed)
<!-- Format:
- When [condition], you typically want [action] (confirmed 3x, YYYY-MM-DD)
-->
- (none yet)

## Wants (explicitly stated)
<!-- Format:
- [pattern description] — confirmed YYYY-MM-DD by [source]
-->
- (none yet)

## Recent Signals (last 7 days, unconfirmed)
<!-- Format:
- [unprompted request] → [action taken] (1st occurrence)
-->
- (none yet)

## Quiet List (user said stop nagging)
<!-- Format:
- [item] — added to quiet list YYYY-MM-DD
-->
- (none yet)
```

## Promotion Rules

| Occurrences | Status | Action |
|------------|--------|--------|
| 1 | Signal | Log to Recent Signals |
| 2 | Signal | Increment count |
| 3+ | Need | Promote to Needs section, ask for confirmation |
| Confirmed | Want | Move to Wants section |

## Quiet List

User can add items: "stop nagging about X"
User can remove: "nag me again about X"
Quiet list items are never surfaced in nudges unless removed.
