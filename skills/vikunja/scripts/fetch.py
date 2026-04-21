#!/usr/bin/env python3
"""
Vikunja Fetch + Cache + Diff 脚本
每次运行：拉取最新任务 → 对比上次缓存 → 报告变化 → 更新缓存
"""
import urllib.request
import json
import os
import sys
from datetime import datetime, timezone, timedelta

CACHE_FILE = os.path.expanduser("~/.vikunja-cache.json")
TOKEN = "tk_3f7b39dc6cf65e27e9a194ab8278db6f335785bd"
BASE = "http://192.168.8.11:3456/api/v1"
BZ = timezone(timedelta(hours=8))  # 北京时间


def load_secrets():
    global TOKEN
    try:
        with open("/opt/data/secrets.txt", "r") as f:
            for line in f:
                if line.strip().startswith("VIKUNJA_API_KEY="):
                    TOKEN = line.strip().split("=", 1)[1].strip()
                    break
    except:
        pass


def api(endpoint):
    req = urllib.request.Request(
        BASE + endpoint,
        headers={"Authorization": f"Bearer {TOKEN}"}
    )
    with urllib.request.urlopen(req, timeout=10) as r:
        return json.loads(r.read())


def load_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE) as f:
            return json.load(f)
    return None


def save_cache(cache):
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)


def bj_now():
    return datetime.now(BZ)


def parse_date(due_str):
    if not due_str or due_str in ("0001-01-01T00:00:00Z", ""):
        return None
    try:
        return datetime.fromisoformat(due_str.replace("Z", "+00:00")).astimezone(BZ).date()
    except:
        return None


def fetch_tasks():
    data = api("/tasks?per_page=100")
    tasks = {}
    for t in data:
        tid = str(t["id"])
        due = parse_date(t.get("due_date"))
        done_date = None
        if t.get("done"):
            # Try to get done date from description or just use today
            done_date = bj_now().strftime("%Y-%m-%d")
        tasks[tid] = {
            "title": t.get("title", ""),
            "done": t.get("done", False),
            "due_date": due.isoformat() if due else None,
            "done_at": done_date,
            "project_id": t.get("project_id"),
        }
    return tasks


def diff(old_tasks, new_tasks):
    old_ids = set(old_tasks.keys())
    new_ids = set(new_tasks.keys())

    newly_completed = [
        tid for tid in old_ids - new_ids
        if old_tasks[tid]["done"] == False
    ]

    newly_added = [
        tid for tid in new_ids - old_ids
    ]

    deleted = [
        tid for tid in old_ids - new_ids
        if old_tasks[tid]["done"] == True
    ]

    today = bj_now().date()

    newly_overdue = []
    for tid in new_ids & old_ids:
        old_due = old_tasks[tid].get("due_date")
        new_due = new_tasks[tid].get("due_date")
        if (old_due and new_due and
            old_due < str(today) == False and  # was not overdue before
            new_due < str(today)):  # is now overdue
            newly_overdue.append(tid)

    # Find newly overdue (was not done, due_date passed)
    for tid in new_ids:
        if not new_tasks[tid]["done"] and new_tasks[tid]["due_date"]:
            if new_tasks[tid]["due_date"] < str(today):
                if old_tasks is None or tid not in old_tasks or not old_tasks[tid].get("_reported_overdue"):
                    newly_overdue.append(tid)

    return {
        "newly_completed": newly_completed,
        "newly_added": newly_added,
        "deleted": deleted,
        "newly_overdue": newly_overdue,
    }


def format_report(new_tasks, diff_result, old_cache=None):
    today = bj_now().date()
    lines = []
    lines.append(f"📋 Vikunja 任务状态 — {bj_now().strftime('%Y-%m-%d %H:%M')} 北京时间\n")

    # Overdue
    overdue = []
    upcoming_3 = []
    active_no_due = []
    completed_recent = []

    for tid, t in sorted(new_tasks.items(), key=lambda x: int(x[0])):
        if t["done"]:
            if old_cache and tid in diff_result.get("newly_completed", []):
                completed_recent.append(tid)
            continue
        due = t.get("due_date")
        if due:
            if due < str(today):
                overdue.append(tid)
            elif (datetime.strptime(due, "%Y-%m-%d").date() - today).days <= 3:
                upcoming_3.append(tid)
        else:
            active_no_due.append(tid)

    if overdue:
        lines.append(f"🔴 已过期（{len(overdue)}）：")
        for tid in overdue:
            t = new_tasks[tid]
            lines.append(f"  #{tid} {t['title']}（截止 {t['due_date']}）")
        lines.append("")

    if completed_recent:
        lines.append(f"✅ 新完成：")
        for tid in completed_recent:
            t = new_tasks[tid]
            done_at = t.get("done_at", "?")
            lines.append(f"  #{tid} {t['title']}（完成于 {done_at}）")
        lines.append("")

    if diff_result.get("newly_added"):
        lines.append(f"🆕 新增任务（{len(diff_result['newly_added'])}）：")
        for tid in diff_result["newly_added"]:
            if tid in new_tasks:
                t = new_tasks[tid]
                lines.append(f"  #{tid} {t['title']}")
        lines.append("")

    if active_no_due:
        lines.append(f"⚪ 进行中无截止日期（{len(active_no_due)}）：")
        for tid in active_no_due[:10]:
            t = new_tasks[tid]
            lines.append(f"  #{tid} {t['title'][:40]}...")
        if len(active_no_due) > 10:
            lines.append(f"  ... 还有 {len(active_no_due)-10} 条")
        lines.append("")

    total = len(new_tasks)
    done_count = sum(1 for t in new_tasks.values() if t["done"])
    lines.append(f"共 {total} 条任务（已完成 {done_count}，进行中 {total-done_count}）")

    return "\n".join(lines)


def format_nudge(new_tasks, diff_result):
    """简洁格式，适合 Telegram push"""
    today = bj_now().date()
    lines = []
    lines.append(f"📋 Vikunja {bj_now().strftime('%m/%d %H:%M')}")

    overdue = []
    completed_recent = []

    for tid, t in sorted(new_tasks.items(), key=lambda x: int(x[0])):
        if t["done"]:
            if tid in diff_result.get("newly_completed", []):
                completed_recent.append(tid)
            continue
        if t.get("due_date") and t["due_date"] < str(today):
            overdue.append(tid)

    if overdue:
        lines.append(f"🔴 过期 {len(overdue)}：")
        for tid in overdue:
            t = new_tasks[tid]
            lines.append(f"  #{tid} {t['title'][:30]}")

    if completed_recent:
        lines.append(f"✅ 新完成 {len(completed_recent)}：")
        for tid in completed_recent:
            t = new_tasks[tid]
            lines.append(f"  #{tid} {t['title'][:30]}")

    if diff_result.get("newly_added"):
        lines.append(f"🆕 新增 {len(diff_result['newly_added'])} 条")

    active = sum(1 for t in new_tasks.values() if not t["done"])
    lines.append(f"⚪ 进行中 {active} 条")

    return "\n".join(lines)


def main():
    load_secrets()

    mode = sys.argv[1] if len(sys.argv) > 1 else "report"
    old_cache = load_cache()
    old_tasks = {}
    if old_cache and "tasks" in old_cache:
        old_tasks = old_cache["tasks"]

    new_tasks = fetch_tasks()

    if mode == "list":
        for tid, t in sorted(new_tasks.items(), key=lambda x: int(x[0])):
            status = "✅" if t["done"] else "⬜"
            due = f"[{t['due_date']}]" if t.get("due_date") else ""
            print(f"{status} #{tid} {due} {t['title']}")
        return

    if mode == "overdue":
        today = bj_now().date()
        for tid, t in sorted(new_tasks.items(), key=lambda x: int(x[0])):
            if not t["done"] and t.get("due_date") and t["due_date"] < str(today):
                print(f"#{tid} {t['title']}（截止 {t['due_date']}）")
        return

    if mode == "snapshot":
        cache = {
            "updated_at": bj_now().isoformat(),
            "total_count": len(new_tasks),
            "tasks": new_tasks,
            "diff_from_previous": {}
        }
        save_cache(cache)
        print(f"✅ 快照已保存：{CACHE_FILE}（{len(new_tasks)} 条任务）")
        return

    if mode == "nudge":
        d = diff(old_tasks, new_tasks)
        report = format_nudge(new_tasks, d)
        print(report)
        # Update cache silently
        cache = {
            "updated_at": bj_now().isoformat(),
            "total_count": len(new_tasks),
            "tasks": new_tasks,
            "diff_from_previous": d
        }
        save_cache(cache)
        return

    # Default: report + diff
    d = diff(old_tasks, new_tasks)
    report = format_report(new_tasks, d, old_cache)
    print(report)

    cache = {
        "updated_at": bj_now().isoformat(),
        "total_count": len(new_tasks),
        "tasks": new_tasks,
        "diff_from_previous": d
    }
    save_cache(cache)
    print(f"\n📁 缓存已更新：{CACHE_FILE}")


if __name__ == "__main__":
    main()
