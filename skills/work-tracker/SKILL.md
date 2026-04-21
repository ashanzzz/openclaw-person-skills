---
name: Work Tracker + Proactive Anticipator
slug: work-tracker
version: 1.1.0
description: "Proactive work lifecycle tracking for 阿山 — monitors: (1) unfinished work from Vikunja; (2) completed work and its context; (3) implied follow-ups from completion patterns; (4) anticipations — what you might need or want based on repetition. Built on Vikunja API + Herme's cronjob + hindsight memory + terminal tools. Inspired by self-improving's tiered memory architecture."
metadata:
  tags: [work-tracking, vikunja, proactive, task-management, lifecycle, hermes-native]
  hermes:
    skills_integrated: [vikunja, proactive-daily-checkin, self-improving]
    tools_used: [cronjob, hindsight_retain, hindsight_recall, terminal, send_message]
    configPaths: [~/work-tracker/]
---

## When to Use

- **New conversation starts** → pull Vikunja state, diff vs baseline, report proactively
- **User says "done" or marks something complete** → verify via Vikunja, log to completions, check follow-ups
- **User asks "what's left?"** → show from `work-queue.md` without re-querying Vikunja
- **User corrects tracking** → log to `corrections.md`, update memory
- **Proactively on heartbeat** → surface items needing attention
- **3x repetition of a pattern** → promote to anticipation rules

## Memory Architecture (Inspired by Self-Improving)

Data lives in `~/work-tracker/` with tiered storage:

```
~/work-tracker/
├── work-queue.md        # HOT: active task snapshot, ≤100 lines, always loaded
├── index.md             # Topic index with line counts
├── heartbeat-state.md    # Heartbeat run markers
├── completions.md        # Completed work log with context
├── follow-ups.md         # Implied next steps from completed work
├── anticipations.md      # Learned: what you might need/want (3x+ patterns)
├── corrections.md        # User corrections log
├── projects/             # Per-project patterns (WARM, ≤200 lines each)
├── domains/             # Domain-specific patterns (WARM)
└── archive/             # COLD: decayed/old patterns
```

**Tier behavior:**
| Tier | File | Limit | Load |
|------|------|-------|------|
| HOT | `work-queue.md` | ≤100 lines | Always on session start |
| WARM | completions, follow-ups, anticipations | ≤200 lines | Load on context match |
| COLD | `archive/` | Unlimited | Load on explicit query |

## Vikunja Integration

**API Base:** `http://192.168.8.11:3456/api/v1`
**Token:** `tk_3f7b39dc6cf65e27e9a194ab8278db6f335785bd`

### API Operations

```python
import urllib.request, json

TOKEN = "tk_3f7b39dc6cf65e27e9a194ab8278db6f335785bd"
BASE = "http://192.168.8.11:3456/api/v1"

def api(endpoint, method='GET', data=None):
    req = urllib.request.Request(BASE + endpoint,
        headers={'Authorization': f'Bearer {TOKEN}'},
        method=method)
    if data:
        req.data = json.dumps(data).encode()
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read())

# Get all tasks
tasks = api('/tasks?per_page=100')

# Get active (done=false)
active = [t for t in tasks if not t['done']]

# Get overdue
from datetime import datetime, timezone, timedelta
bj = timezone(timedelta(hours=8))
today = datetime.now(bj).date()
overdue = [t for t in active if
    t['due_date'] not in (None, '0001-01-01T00:00:00Z') and
    datetime.fromisoformat(t['due_date'].replace('Z','+00:00')).astimezone(bj).date() < today]

# Update task done=true
api(f"/tasks/{task_id}", 'PUT', {'done': True})

# Create follow-up task
api('/tasks', 'POST', {
    'title': 'Follow-up for: ' + parent_title,
    'project_id': project_id,
    'due_date': None
})
```

## Session Start Workflow (Proactive Diff)

```
1. GET /tasks from Vikunja → current state
2. Load ~/work-tracker/work-queue.md → last snapshot
3. Diff vs baseline:
   - new_ids = current_ids - baseline_ids        → 🆕 newly added
   - done_ids = baseline_ids - current_ids      → ✅ newly completed
   - missing_ids = baseline_ids - current_ids    → 🗑️ deleted/moved
   - newly_overdue = items now past due_date     → 🔴 newly overdue
4. Report proactively to user (don't wait to be asked)
5. Update work-queue.md snapshot
6. If done items → log to completions.md + check follow-ups
```

## Task Completion Workflow

```
1. User marks task done → PUT /tasks/{id} {"done": true}
2. Log to completions.md:
   - Task ID, title, project
   - Completion timestamp (北京时间)
   - Context: what this was about
   - Follow-up needed: yes/no/maybe + specific item
3. Check follow-ups.md for implied next steps
4. Prompt user: "Done! What's next?" if no follow-up found
5. If this reveals a new chain pattern (A→B) → log to follow-ups.md
6. Update anticipations.md if this suggests user intent
```

## Anticipation Learning (Hermes Native)

Anticipations are what you **might need** before you ask — learned from repetition:

| Occurrences | Status | Action |
|-----------|--------|--------|
| 1 | Signal | Log to anticipations.md "Recent Signals" |
| 2 | Signal | Increment count |
| 3+ | Need | Promote to "Needs" section, surface to user |
| Confirmed | Want | Move to "Wants", never decay |

**Examples:**
- "每次完成有声书文本任务，用户接下来会问批量合成" → promote after 3x
- "用户说'还有别的吗'之后，经常会想看过期任务" → track
- "用户完成 DSM 相关任务后，可能会想测外网入口" → project-domain pattern

**Learning signals:**
- User unpromptedly asks for X after completing Y → potential new anticipation
- User says "I was just about to ask about that" → strong signal
- Same follow-up suggested 3x and accepted → confirmed pattern
- User says "stop nagging about X" → add to Quiet List

## Proactive Nudge Format

```
📊 工作追踪 — {YYYY-MM-DD HH:MM} 北京时间

🔴 已过期（{N}）：
  #{id} {标题}（截止 {日期}）

🟡 今日到期（{N}）：
  #{id} {标题}

🟠 即将到期（3天内，{N}）：
  #{id} {标题}（截止 {日期}）

⚪ 进行中无截止日期（{N}）：
  #{id} {标题}...

✅ 新完成（since last check，{N}）：
  #{id} {标题}（完成于 {日期}）

💡 建议跟进：
  #id "{标题}" 已完成 → 建议：{跟进事项}

📝 待你确认：
  Anticipating: {用户可能想要什么} — 请回复"是的"或"不是"
```

## Hermes Tool Integration

### Cronjob (Daily Morning Nudge)
```python
cronjob(action='create',
    name='work-tracker 每日早8点推送',
    prompt='''你是阿山的工作追踪助手。每天早8点（北京时间）执行 Vikunja 状态推送。

执行步骤：
1. GET http://192.168.8.11:3456/api/v1/tasks?per_page=100
2. 分析过期/今日到期/3天内到期/新完成
3. 格式化成中文主动推送（不用等用户问）
4. 检查 anticipations.md — 如果有3x+ pattern，要问用户"你是不是还想..."
5. 发送目标：telegram:6213495524

技能：vikunja, work-tracker''',
    schedule='0 8 * * *',
    skills=['vikunja', 'work-tracker'],
    deliver='telegram:6213495524')
```

### Hindsight Integration
```python
# On session start — recall relevant memories
hindsight_recall(query="阿山 work tracking patterns preferences follow-ups")
# → Gets injected into context automatically

# After completion — retain learning
hindsight_retain(
    content="Task #37 'Gradio/FastAPI接口' completed → 阿山接下来想看批处理方案",
    context="work-tracker completion pattern"
)

# On correction — reflect
hindsight_retain(
    content="Correction: #61 not done yet, still in progress → update tracking",
    context="user correction"
)
```

### Terminal Tool (Snapshot & Diff)
```bash
python3 ~/work-tracker/work-tracker.py nudge    # Show current status
python3 ~/work-tracker/work-tracker.py snapshot # Save snapshot
python3 ~/work-tracker/work-tracker.py list     # List active tasks
python3 ~/work-tracker/work-tracker.py overdue  # Show overdue only
python3 ~/work-tracker/work-tracker.py completed # Show recently done
```

## Setup

If `~/work-tracker/` does not exist, run `setup.md`.

```bash
mkdir -p ~/work-tracker/{projects,domains,archive,templates,references}
# Then initialize from setup.md
```

## Core Rules

### 1. Vikunja is Source of Truth
- Always verify via API before claiming task state
- If Vikunja unreachable → use last snapshot, note staleness

### 2. Proactive But Not Annoying
- Same item nudged max twice per day
- Quiet List: items user said "stop nagging" — never surface
- Escalate: silent → soft nudge → hard nudge

### 3. Follow-Up Intelligence
- Complete "build/develop/implement/create" → suggest "test/verify"
- Complete in project X → check if other X tasks stalled
- Chain: if A→B→C learned, and A completes, prompt about B

### 4. Corrections → Smarter
- User correcting state → log to corrections.md
- Evaluate: does this reveal a pattern?
- Never make same nudge error twice

### 5. Anticipation Transparency
- Cite source: "Anticipating X (from pattern: Y, 3x)"
- User can override: "don't anticipate that"
- Never act on anticipation — always confirm first

## Scope

**ONLY:**
- Read Vikunja API for task state
- Store lifecycle data in ~/work-tracker/
- Log completions, follow-ups, anticipations, corrections
- Surface items needing attention proactively
- Learn from explicit signals and 3x+ repetition

**NEVER:**
- Modify Vikunja tasks without explicit instruction
- Infer intent from silence
- Auto-create tasks — always prompt
- Delete historical records without asking
