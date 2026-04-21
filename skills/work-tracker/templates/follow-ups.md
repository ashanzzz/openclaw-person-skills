# Follow-Ups — Template

Append to `~/work-tracker/follow-ups.md`.

```markdown
# Follow-Up Patterns

## Implied Follow-Ups (learned)
| Completed Task Contains | Implied Follow-Up |
|-----------------------|-------------------|
| build / implement / develop / create | test / verify |
| finish / complete | document |
| deploy / release | check health / monitor |
| submit / send | track result |
| update / change / modify | review / test |

## Pending Follow-Ups
| Parent Task ID | Parent Title | Follow-Up Task | Status |
|---------------|--------------|-----------------|--------|
| — | — | — | pending |

## Chain Follow-Ups (learned sequences)
- A → B → C: [sequence description]
```

## Guidelines

- When a task completes, check implied follow-ups table
- If a pattern repeats 3x, add it to the implied follow-ups table
- Chain follow-ups: if A→B→C learned, flag B when A completes
- Never auto-create tasks — always prompt user first
