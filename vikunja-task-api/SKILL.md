---
name: vikunja-task-api
version: 2.0.0
description: Manage Vikunja projects and tasks (overdue/due/today), mark done, and get quick summaries via the Vikunja API.
homepage: https://vikunja.io/
metadata: {"clawdbot":{"emoji":"📋","requires":{"bins":["curl","jq"],"env":["VIKUNJA_URL"],"optionalEnv":["VIKUNJA_TOKEN","VIKUNJA_USERNAME","VIKUNJA_PASSWORD"]},"primaryEnv":"VIKUNJA_TOKEN"}}
---

# Vikunja Fast Skill (v2 API)

Use Vikunja as the **source of truth** for all task management. This skill supersedes any internal working-buffer tracking for user-visible tasks.

## API Base

- **Base URL**: `$VIKUNJA_URL/api/v1` (auto-normalized)
- **Auth**: JWT Bearer token (`Authorization: Bearer <token>`)
- **Token acquisition**: `POST /login` (username field is `username`)

## Critical API Differences (Must Remember)

| Operation | Correct Method |
|-----------|---------------|
| Create project | `PUT /projects` (**PUT**, not POST) |
| Update project | `POST /projects/{id}` (**POST**) |
| Create task | `PUT /projects/{id}/tasks` (**PUT**, not POST) |
| Update task (including mark done) | `POST /tasks/{id}` |
| Get all tasks | `GET /tasks` (**not** `/tasks/all`) |
| Delete task | `DELETE /tasks/{id}` |
| Move task to kanban bucket | `POST /projects/{project}/views/{view}/buckets/{bucket}/tasks` |

## Setup

```bash
# Environment variables (recommended: write to secure/api-fillin.env)
VIKUNJA_URL=http://192.168.8.11:3456
VIKUNJA_TOKEN=tk_xxxx   # API Token or JWT
```

## Quick Commands

```bash
# Login to get JWT (if you only have username/password)
curl -X POST "$VIKUNJA_URL/login" \
  -H "Content-Type: application/json" \
  -d '{"username":"USER","password":"PASS","long_token":true}' | jq

# List all projects
curl -s "$VIKUNJA_URL/projects" -H "Authorization: Bearer $VIKUNJA_TOKEN" | jq '.[] | {id,title}'

# List all open tasks
curl -s "$VIKUNJA_URL/tasks" -H "Authorization: Bearer $VIKUNJA_TOKEN" \
  | jq '.[] | select(.done == false) | {id,title,due_date:.due_date,project_id}'

# Create project (PUT /projects)
curl -X PUT "$VIKUNJA_URL/projects" \
  -H "Authorization: Bearer $VIKUNJA_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"Project Name","description":"","identifier":"","hex_color":""}' | jq '{id,title}'

# Create task in project (PUT /projects/{id}/tasks)
curl -X PUT "$VIKUNJA_URL/projects/9/tasks" \
  -H "Authorization: Bearer $VIKUNJA_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"Task Title","description":"","due_date":"2026-04-30T23:59:00Z"}' | jq '{id,title}'

# Mark task done (POST /tasks/{id})
curl -X POST "$VIKUNJA_URL/tasks/123" \
  -H "Authorization: Bearer $VIKUNJA_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"done":true}' | jq '{id,done,done_at}'

# Update task (POST /tasks/{id}, can change project_id to move task)
curl -X POST "$VIKUNJA_URL/tasks/123" \
  -H "Authorization: Bearer $VIKUNJA_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"project_id":9,"title":"New Title"}' | jq '{id,project_id,title}'

# Delete task (DELETE /tasks/{id})
curl -X DELETE "$VIKUNJA_URL/tasks/123" \
  -H "Authorization: Bearer $VIKUNJA_TOKEN"

# Bulk update tasks
curl -X POST "$VIKUNJA_URL/tasks/bulk" \
  -H "Authorization: Bearer $VIKUNJA_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"tasks":[{"id":1,"done":true},{"id":2,"done":true}]}' | jq
```

## Helper CLI (vikunja.sh)

```bash
# List open tasks (sorted by due date)
vikunja.sh list --filter 'done = false'

# Overdue tasks
vikunja.sh overdue

# Due today
vikunja.sh due-today

# View task details
vikunja.sh show 123

# Mark done
vikunja.sh done 123

# Create task
vikunja.sh create 9 "New Task Title"

# Delete task
vikunja.sh delete 123
```

## Task Display Format

Each task output format:
```
<EMOJI> <DUE_DATE> - #<ID> <TASK>
```

- Emoji: first character of project title (first non-alphanumeric token for Chinese/English titles)
- Default emoji when none: 🔨
- No due date shows `(no due)`

## Filtering Syntax

Vikunja filter examples:
```
done = false
done = false && due_date < now
done = false && project_id = 9
done = false && due_date >= now/d && due_date < now/d + 1d
```

Full docs: https://vikunja.io/docs/filters/

## Task Model (Important Fields)

```json
{
  "id": 123,
  "title": "Task Title",
  "description": "",
  "done": false,
  "done_at": null,
  "due_date": "2026-04-30T15:59:00Z",
  "project_id": 9,
  "repeat_after": 0,
  "priority": 0,
  "start_date": "0001-01-01T00:00:00Z",
  "end_date": "0001-01-01T00:00:00Z",
  "hex_color": "",
  "percent_done": 0,
  "created": "2026-03-31T12:00:00Z",
  "updated": "2026-03-31T12:00:00Z"
}
```

Note: `due_date` = `0001-01-01T00:00:00Z` means no deadline.
