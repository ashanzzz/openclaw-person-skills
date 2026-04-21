# Vikunja API Quick Reference — Work Tracker

## Base

`http://192.168.8.11:3456/api/v1`

## Authentication

Header: `Authorization: Bearer tk_3f7b39dc6cf65e27e9a194ab8278db6f335785bd`

## Key Endpoints

| Action | Method | Endpoint | Body |
|--------|--------|----------|------|
| List all tasks | GET | `/tasks?per_page=100` | — |
| List tasks (filter) | GET | `/tasks?project_id={id}&done=false` | — |
| Get task | GET | `/tasks/{id}` | — |
| Create task | POST | `/tasks` | `{"title":"...","project_id":N,"due_date":"..."}` |
| Update task | PUT | `/tasks/{id}` | `{"done": true}` |
| Delete task | DELETE | `/tasks/{id}` | — |
| List projects | GET | `/projects` | — |
| Get project | GET | `/projects/{id}` | — |
| List labels | GET | `/labels` | — |

## Task Object

```json
{
  "id": 38,
  "title": "有声书流水线：文本分章/断句/分段策略",
  "done": false,
  "due_date": "0001-01-01T00:00:00Z",
  "priority": 0,
  "labels": null,
  "project_id": 10,
  "created": "2026-03-23T09:08:10Z",
  "updated": "2026-04-07T13:38:29Z",
  "start_date": "0001-01-01T00:00:00Z"
}
```

## Key Dates

- `due_date == "0001-01-01T00:00:00Z"` → no due date set
- `due_date < today` → overdue
- `due_date == today` → due today
- `due_date <= today + 3 days` → due soon

## Work Tracker Patterns

```python
# Fetch all active tasks (done=false)
tasks = GET /tasks?per_page=100
active = [t for t in tasks if not t['done']]

# Fetch recently completed
completed = [t for t in tasks if t['done']]
recent_completed = [t for t in completed if was_updated_recently(t)]

# Detect overdue
from datetime import datetime, timezone, timedelta
today = datetime.now(timezone(timedelta(hours=8)))  # Beijing
overdue = [t for t in active
           if t['due_date'] not in (None, '0001-01-01T00:00:00Z')
           and parse(t['due_date']) < today]

# Diff vs baseline
baseline_ids = {38, 39, 40, ...}  # from work-queue.md
current_ids = {t['id'] for t in current_tasks}
new_ids = current_ids - baseline_ids
done_ids = baseline_ids - {t['id'] for t in current_tasks if not t['done']}
```
