#!/usr/bin/env python3
# Work Tracker — Vikunja Quick Query Script
# Usage: python3 work-tracker.py [command] [args]
#
# Commands:
#   list              List all active tasks
#   overdue           List overdue tasks
#   completed         List recently completed tasks
#   due-soon [days]   List tasks due within N days (default: 7)
#   nudge             Format current status for user nudge
#   snapshot          Save current Vikunja state to work-queue.md

import sys
import json
import urllib.request
import urllib.error
from datetime import datetime, timezone, timedelta
from pathlib import Path

VIKUNJA_BASE = "http://192.168.8.11:3456/api/v1"
TOKEN = "tk_3f7b39dc6cf65e27e9a194ab8278db6f335785bd"
WORK_TRACKER_DIR = Path.home() / "work-tracker"

# Colors
RED = '\033[0;31m'
YELLOW = '\033[1;33m'
GREEN = '\033[0;32m'
CYAN = '\033[0;36m'
NC = '\033[0m'

def vikunja_api(endpoint, method='GET', data=None):
    url = VIKUNJA_BASE + endpoint
    headers = {
        'Authorization': f'Bearer {TOKEN}',
        'Content-Type': 'application/json'
    }
    req = urllib.request.Request(url, headers=headers, method=method)
    if data:
        req.data = json.dumps(data).encode()
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        print(f"HTTP Error {e.code}: {e.reason}", file=sys.stderr)
        return None
    except urllib.error.URLError as e:
        print(f"URL Error: {e.reason}", file=sys.stderr)
        return None

def beijing_now():
    return datetime.now(timezone(timedelta(hours=8)))

def cmd_list(tasks):
    print(f"{CYAN}=== Active Tasks ==={NC}")
    active = [t for t in tasks if not t['done']]
    print(f"Total active: {len(active)}\n")
    for t in sorted(active, key=lambda x: x.get('due_date', '9999')):
        due = t.get('due_date', 'none')
        if due in (None, '0001-01-01T00:00:00Z'):
            due = 'no due date'
        print(f"  #{t['id']} [{t['project_id']}] {t['title'][:50]} | due: {due}")

def cmd_overdue(tasks):
    print(f"{RED}=== Overdue Tasks ==={NC}")
    today = beijing_now().date()
    active = [t for t in tasks if not t['done']]
    overdue = []
    for t in active:
        due = t.get('due_date', '')
        if due and due != '0001-01-01T00:00:00Z':
            d = datetime.fromisoformat(due.replace('Z', '+00:00')).astimezone(timezone(timedelta(hours=8))).date()
            if d < today:
                overdue.append((d, t))
    if overdue:
        for d, t in sorted(overdue):
            print(f"  #{t['id']} {t['title'][:50]} | was due: {d}")
    else:
        print("  (none)")

def cmd_completed(tasks):
    print(f"{GREEN}=== Recently Completed ==={NC}")
    done = [t for t in tasks if t['done']]
    print(f"Total completed (in list): {len(done)}\n")
    for t in sorted(done, key=lambda x: x.get('updated', ''), reverse=True)[:10]:
        upd = t.get('updated', 'unknown')
        print(f"  #{t['id']} {t['title'][:50]} | updated: {upd[:10]}")

def cmd_duesoon(tasks, days=7):
    print(f"{YELLOW}=== Due Within {days} Days ==={NC}")
    future = beijing_now().date() + timedelta(days=days)
    active = [t for t in tasks if not t['done']]
    soon = []
    for t in active:
        due = t.get('due_date', '')
        if due and due != '0001-01-01T00:00:00Z':
            d = datetime.fromisoformat(due.replace('Z', '+00:00')).astimezone(timezone(timedelta(hours=8))).date()
            if d <= future:
                soon.append((d, t))
    if soon:
        for d, t in sorted(soon):
            print(f"  #{t['id']} {t['title'][:50]} | due: {d}")
    else:
        print("  (none)")

def cmd_nudge(tasks):
    today = beijing_now().date()
    active = [t for t in tasks if not t['done']]
    done = [t for t in tasks if t['done']]

    overdue = []
    due_soon = []
    no_due = []
    for t in active:
        due = t.get('due_date', '')
        if not due or due == '0001-01-01T00:00:00Z':
            no_due.append(t)
        else:
            d = datetime.fromisoformat(due.replace('Z', '+00:00')).astimezone(timezone(timedelta(hours=8))).date()
            if d < today:
                overdue.append((d, t))
            elif d <= today + timedelta(days=3):
                due_soon.append((d, t))

    recent_done = sorted(done, key=lambda x: x.get('updated', ''), reverse=True)[:5]

    lines = [f"📊 Work Status — {today} 北京时间", ""]
    lines.append(f"🔴 Overdue ({len(overdue)}):")
    if overdue:
        for d, t in sorted(overdue):
            lines.append(f"  #{t['id']} {t['title'][:40]}（截止 {d}）")
    else:
        lines.append("  （无）")

    lines.append(f"\n🟠 Due Soon ({len(due_soon)}):")
    if due_soon:
        for d, t in sorted(due_soon):
            lines.append(f"  #{t['id']} {t['title'][:40]}（截止 {d}）")
    else:
        lines.append("  （无）")

    lines.append(f"\n⚪ Active No-Due-Date ({len(no_due)}):")
    if no_due:
        for t in no_due[:10]:
            lines.append(f"  #{t['id']} {t['title'][:40]}")
        if len(no_due) > 10:
            lines.append(f"  ... 还有 {len(no_due)-10} 条")
    else:
        lines.append("  （无）")

    lines.append(f"\n✅ Recently Completed ({len(recent_done)}):")
    if recent_done:
        for t in recent_done:
            upd = t.get('updated', 'unknown')[:10]
            lines.append(f"  #{t['id']} {t['title'][:40]}（完成于 {upd}）")
    else:
        lines.append("  （无）")

    print('\n'.join(lines))

def cmd_snapshot(tasks):
    print(f"{CYAN}Saving snapshot to work-queue.md...{NC}")
    WORK_TRACKER_DIR.mkdir(parents=True, exist_ok=True)
    output = WORK_TRACKER_DIR / "work-queue.md"
    now = beijing_now()
    today = now.date()

    active = [t for t in tasks if not t['done']]
    overdue = []
    for t in active:
        due = t.get('due_date', '')
        if due and due != '0001-01-01T00:00:00Z':
            d = datetime.fromisoformat(due.replace('Z', '+00:00')).astimezone(timezone(timedelta(hours=8))).date()
            if d < today:
                overdue.append((d, t))

    lines = [
        '# Work Queue Snapshot',
        '',
        f'Last updated: {now.strftime("%Y-%m-%d %H:%M")} Beijing',
        '',
        '## Active Tasks',
        '| ID | Title | Project | Due | Updated |',
        '|----|-------|---------|-----|--------|',
    ]
    for t in sorted(active, key=lambda x: x.get('due_date', '9999')):
        due = t.get('due_date', '')
        if due == '0001-01-01T00:00:00Z':
            due = '—'
        else:
            due = due[:10]
        upd = t.get('updated', '')[:10]
        lines.append(f"| {t['id']} | {t['title'][:40]} | {t['project_id']} | {due} | {upd} |")

    lines.extend(['', '## Overdue', '| ID | Title | Due Date |', '|----|-------|----------|'])
    if overdue:
        for d, t in sorted(overdue):
            lines.append(f"| {t['id']} | {t['title'][:40]} | {d} |")
    else:
        lines.append("| — | — | — |")

    lines.extend([
        '',
        '## Snapshot Baseline',
        f'- Total active: {len(active)}',
        f'- Overdue: {len(overdue)}',
        f'- Last diff run: {now.strftime("%Y-%m-%d %H:%M")}',
    ])

    output.write_text('\n'.join(lines), encoding='utf-8')
    print(f"Saved to {output} ({len(active)} active, {len(overdue)} overdue)")

def main():
    # Fetch all tasks
    tasks = vikunja_api('/tasks?per_page=100')
    if tasks is None:
        print("Failed to fetch tasks from Vikunja", file=sys.stderr)
        sys.exit(1)

    cmd = sys.argv[1] if len(sys.argv) > 1 else 'nudge'

    if cmd == 'list':
        cmd_list(tasks)
    elif cmd == 'overdue':
        cmd_overdue(tasks)
    elif cmd == 'completed':
        cmd_completed(tasks)
    elif cmd == 'due-soon':
        days = int(sys.argv[2]) if len(sys.argv) > 2 else 7
        cmd_duesoon(tasks, days)
    elif cmd == 'nudge':
        cmd_nudge(tasks)
    elif cmd == 'snapshot':
        cmd_snapshot(tasks)
    elif cmd in ('help', '--help', '-h'):
        print("Usage: work-tracker.py [command]")
        print("Commands: list, overdue, completed, due-soon [days], nudge, snapshot")
    else:
        cmd_nudge(tasks)

if __name__ == '__main__':
    main()
