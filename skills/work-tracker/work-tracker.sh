#!/bin/bash
# Work Tracker — Vikunja Quick Query Script
# Usage: ./work-tracker.sh [command] [args]
#
# Commands:
#   list              List all active tasks
#   overdue           List overdue tasks
#   completed         List recently completed tasks
#   due-soon [days]   List tasks due within N days (default: 7)
#   diff              Show changes since last snapshot
#   nudge             Format current status for user nudge
#   snapshot          Save current Vikunja state to work-queue.md

VIKUNJA_BASE="http://192.168.8.11:3456/api/v1"
TOKEN="tk_3f7b39dc6cf65e27e9a194ab8278db6f335785bd"
WORK_TRACKER_DIR="${WORK_TRACKER_DIR:-$HOME/work-tracker}"

# Colors (for terminal output)
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Helper: make API request
vikunja_api() {
  local method="${1:-GET}"
  local endpoint="$2"
  local data="$3"
  if [ -n "$data" ]; then
    curl -s -X "$method" \
      -H "Authorization: Bearer $TOKEN" \
      -H "Content-Type: application/json" \
      -d "$data" \
      "$VIKUNJA_BASE$endpoint"
  else
    curl -s -X "$method" \
      -H "Authorization: Bearer $TOKEN" \
      "$VIKUNJA_BASE$endpoint"
  fi
}

# Helper: parse date (BSD/macOS compatible)
parse_date() {
  local date_str="$1"
  # Convert ISO date to readable format
  echo "$date_str" | sed 's/T/ /;s/Z//'
}

# Command: list
cmd_list() {
  echo -e "${CYAN}=== Active Tasks ===${NC}"
  vikunja_api GET "/tasks?per_page=100" | \
    python3 -c "
import sys, json
tasks = json.load(sys.stdin)
active = [t for t in tasks if not t['done']]
print(f'Total active: {len(active)}\\n')
for t in sorted(active, key=lambda x: x.get('due_date','9999')):
    due = t.get('due_date','none')
    if due == '0001-01-01T00:00:00Z': due = 'no due date'
    print(f\"  #{t['id']} [{t['project_id']}] {t['title'][:50]} | due: {due}\")
"
}

# Command: overdue
cmd_overdue() {
  echo -e "${RED}=== Overdue Tasks ===${NC}"
  vikunja_api GET "/tasks?per_page=100" | \
    python3 -c "
import sys, json
from datetime import datetime, timezone, timedelta

tasks = json.load(sys.stdin)
today = datetime.now(timezone(timedelta(hours=8))).date()
active = [t for t in tasks if not t['done']]
overdue = []
for t in active:
    due = t.get('due_date','')
    if due and due != '0001-01-01T00:00:00Z':
        d = datetime.fromisoformat(due.replace('Z','+00:00')).astimezone(timezone(timedelta(hours=8))).date()
        if d < today:
            overdue.append((d, t))
for d, t in sorted(overdue):
    print(f\"  #{t['id']} {t['title'][:50]} | was due: {d}\")
if not overdue: print('  (none)')
"
}

# Command: completed
cmd_completed() {
  echo -e "${GREEN}=== Recently Completed ===${NC}"
  vikunja_api GET "/tasks?per_page=100" | \
    python3 -c "
import sys, json
tasks = json.load(sys.stdin)
done = [t for t in tasks if t['done']]
print(f'Total completed (in list): {len(done)}\\n')
for t in sorted(done, key=lambda x: x.get('updated',''), reverse=True)[:10]:
    upd = t.get('updated','unknown')
    print(f\"  #{t['id']} {t['title'][:50]} | updated: {upd[:10]}\")
"
}

# Command: due-soon
cmd_duesoon() {
  local days="${1:-7}"
  echo -e "${YELLOW}=== Due Within $days Days ===${NC}"
  vikunja_api GET "/tasks?per_page=100" | \
    python3 -c "
import sys, json
from datetime import datetime, timezone, timedelta

tasks = json.load(sys.stdin)
future = datetime.now(timezone(timedelta(hours=8))).date() + timedelta(days=$days)
active = [t for t in tasks if not t['done']]
soon = []
for t in active:
    due = t.get('due_date','')
    if due and due != '0001-01-01T00:00:00Z':
        d = datetime.fromisoformat(due.replace('Z','+00:00')).astimezone(timezone(timedelta(hours=8))).date()
        if d <= future:
            soon.append((d, t))
for d, t in sorted(soon):
    print(f\"  #{t['id']} {t['title'][:50]} | due: {d}\")
if not soon: echo '  (none)'
"
}

# Command: nudge
cmd_nudge() {
  vikunja_api GET "/tasks?per_page=100" | \
    python3 -c "
import sys, json
from datetime import datetime, timezone, timedelta

tasks = json.load(sys.stdin)
today = datetime.now(timezone(timedelta(hours=8))).date()
active = [t for t in tasks if not t['done']]
done = [t for t in tasks if t['done']]

overdue = []
due_soon = []
no_due = []
for t in active:
    due = t.get('due_date','')
    if not due or due == '0001-01-01T00:00:00Z':
        no_due.append(t)
    else:
        d = datetime.fromisoformat(due.replace('Z','+00:00')).astimezone(timezone(timedelta(hours=8))).date()
        if d < today:
            overdue.append((d, t))
        elif d <= today + timedelta(days=3):
            due_soon.append((d, t))

recent_done = sorted(done, key=lambda x: x.get('updated',''), reverse=True)[:5]

print(f'''📊 Work Status — {today} 北京时间

🔴 Overdue ({len(overdue)}):''')
for d, t in sorted(overdue):
    print(f\"  #{t['id']} {t['title'][:40]}（截止 {d}）\")

print(f'\\n🟠 Due Soon ({len(due_soon)}):')
for d, t in sorted(due_soon):
    print(f\"  #{t['id']} {t['title'][:40]}（截止 {d}）\")

print(f'\\n⚪ Active No-Due-Date ({len(no_due)}):')
for t in no_due[:10]:
    print(f\"  #{t['id']} {t['title'][:40]}\")
if len(no_due) > 10: print(f\"  ... 还有 {len(no_due)-10} 条\")

print(f'\\n✅ Recently Completed ({len(recent_done)}):')
for t in recent_done:
    upd = t.get('updated','unknown')[:10]
    print(f\"  #{t['id']} {t['title'][:40]}（完成于 {upd}）\")
"
}

# Command: snapshot
cmd_snapshot() {
  echo -e "${CYAN}Saving snapshot to work-queue.md...${NC}"
  mkdir -p "$WORK_TRACKER_DIR"
  local output="$WORK_TRACKER_DIR/work-queue.md"
  vikunja_api GET "/tasks?per_page=100" | \
    python3 -c "
import sys, json
from datetime import datetime, timezone, timedelta

tasks = json.load(sys.stdin)
now = datetime.now(timezone(timedelta(hours=8)))
today = now.date()
active = [t for t in tasks if not t['done']]
done = [t for t in tasks if t['done']]

overdue = []
for t in active:
    due = t.get('due_date','')
    if due and due != '0001-01-01T00:00:00Z':
        d = datetime.fromisoformat(due.replace('Z','+00:00')).astimezone(timezone(timedelta(hours=8))).date()
        if d < today:
            overdue.append((d, t))

lines = [
    '# Work Queue Snapshot',
    '',
    f'Last updated: {now.strftime(\"%Y-%m-%d %H:%M\")} Beijing',
    '',
    '## Active Tasks',
    '| ID | Title | Project | Due | Updated |',
    '|----|-------|---------|-----|--------|',
]
for t in sorted(active, key=lambda x: x.get('due_date','9999')):
    due = t.get('due_date','')
    if due == '0001-01-01T00:00:00Z': due = '—'
    else: due = due[:10]
    upd = t.get('updated','')[:10]
    lines.append(f\"| {t['id']} | {t['title'][:40]} | {t['project_id']} | {due} | {upd} |\")
lines.append('')
lines.append('## Overdue')
lines.append('| ID | Title | Due Date |')
lines.append('|----|-------|----------|')
if overdue:
    for d, t in sorted(overdue):
        lines.append(f\"| {t['id']} | {t['title'][:40]} | {d} |\")
else:
    lines.append('| — | — | — |')
lines.append('')
lines.append('## Snapshot Baseline')
lines.append(f'- Total active: {len(active)}')
lines.append(f'- Overdue: {len(overdue)}')
lines.append(f'- Last diff run: {now.strftime(\"%Y-%m-%d %H:%M\")}')

with open('$output', 'w') as f:
    f.write('\\n'.join(lines))
print(f'Saved to $output ({len(active)} active, {len(overdue)} overdue)')
"
}

# Main dispatch
case "${1:-}" in
  list)       cmd_list ;;
  overdue)    cmd_overdue ;;
  completed)  cmd_completed ;;
  due-soon)   cmd_duesoon "$2" ;;
  nudge)      cmd_nudge ;;
  snapshot)   cmd_snapshot ;;
  help|--help|-h)
    echo "Usage: $0 [command]"
    echo "Commands: list, overdue, completed, due-soon [days], nudge, snapshot"
    ;;
  *)          cmd_nudge ;;
esac
