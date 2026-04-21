# Setup — Work Tracker + Proactive Anticipator

## First-Time Setup

### 1. Create Directory Structure

```bash
mkdir -p ~/work-tracker/{projects,domains,archive,references,templates}
```

### 2. Initialize Core Files

Create `~/work-tracker/work-queue.md` using the template:

```markdown
# Work Queue Snapshot

Last updated: never

## Active Tasks
| ID | Title | Project | Due | Updated | Status |
|----|-------|---------|-----|---------|--------|

## Overdue
| ID | Title | Due Date |
|----|-------|----------|

## Snapshot Baseline
- Total active: 0
- Overdue: 0
- Last diff run: never
```

Create `~/work-tracker/completions.md`:

```markdown
# Completions Log

<!-- Format:
## YYYY-MM-DD
- [#id] "Task title" — project: {name}
  Context: what this was about
  Follow-up needed: yes/no/maybe
-->

## 2026-01-01 — Session Start
- Work Tracker initialized
```

Create `~/work-tracker/follow-ups.md`:

```markdown
# Follow-Up Patterns

Learned from completed tasks:

## Implied Follow-Ups
| Completed Task Contains | Implied Follow-Up |
|-----------------------|-------------------|
| build / implement / develop / create | test / verify |
| finish / complete | document |
| deploy / release | check health / monitor |
| submit / send | track result |
| update / change / modify | review / test |

## Pending Follow-Ups
| Parent Task ID | Follow-Up Task | Status |
|---------------|----------------|--------|
```

Create `~/work-tracker/anticipations.md`:

```markdown
# Anticipations — What You Might Need

## Needs (expressed 3x+)
<!-- Format: - [condition] → [typical user action] (count) -->

## Wants (confirmed explicitly)
<!-- Format: - [pattern] — confirmed YYYY-MM-DD -->

## Recent (last 7 days)
<!-- Format: - [unprompted request] → [action taken] -->
```

Create `~/work-tracker/corrections.md`:

```markdown
# Corrections Log

<!-- Format:
## YYYY-MM-DD HH:MM
- Said: "[incorrect claim]"
  Reality: "[actual state]"
  Lesson: "[what to do differently]"
-->
```

Create `~/work-tracker/heartbeat-state.md`:

```markdown
# Work Tracker Heartbeat State

last_heartbeat_started_at: never
last_reviewed_change_at: never
last_heartbeat_result: never

## Last actions
- none yet
```

Create `~/work-tracker/index.md`:

```markdown
# Work Tracker Index

## HOT
- work-queue.md: 0 lines

## WARM
- completions.md: 0 lines
- follow-ups.md: 0 lines
- anticipations.md: 0 lines

## COLD
- archive/: 0 files

Last update: never
```

### 3. Take Initial Vikunja Snapshot

Pull current Vikunja state and populate work-queue.md:

```bash
# Fetch all tasks from Vikunja
curl -s -H "Authorization: Bearer <token>" \
  "http://192.168.8.11:3456/api/v1/tasks?per_page=100" \
  > ~/work-tracker/vikunja-baseline.json
```

Parse and populate work-queue.md with:
- All `done=false` tasks → Active Tasks table
- All `done=true` tasks → Completions Log
- Tasks with `due_date < today` → Overdue table
- Set `Last updated` to current Beijing time
- Set `Total active` and `Overdue` counts

### 4. Add to HEARTBEAT.md (Optional)

Add to workspace `HEARTBEAT.md` for automatic maintenance:

```markdown
## Work Tracker Check

- Read `./skills/work-tracker/heartbeat-rules.md`
- Use `~/work-tracker/heartbeat-state.md` for last-run markers
- If Vikunja state changed since last run → update work-queue.md
- Return `HEARTBEAT_OK` if nothing needs attention
```

### 5. Verification

Run "work status" to confirm setup:

```
📊 Work Tracker

Active tasks: N
Overdue: N
Completions logged: N
Follow-ups pending: N
Last snapshot: YYYY-MM-DD HH:MM
```

## Migrating from Baseline

If you have an existing task baseline in memory (e.g., from proactive-daily-checkin):

1. Convert baseline IDs to full task list via Vikunja API
2. Populate work-queue.md with actual task data
3. Import any existing overdue/completed items to completions.md
4. Delete old baseline from memory to avoid confusion
