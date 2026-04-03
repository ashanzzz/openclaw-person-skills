#!/usr/bin/env python3
"""
audit_books.py
复核九本书切片与笔记一致性。
"""
import os
import re
import json

NOTES_BASE = "/root/.openclaw/workspace/kb/books-notes"
BOOKS = [
    "驱动力",
    "人性的弱点",
    "格鲁夫给经理人的第一课",
    "第五项修炼",
    "管理的常识",
    "精益思想",
    "领导梯队",
    "丰田模式",
    "高效能人士的七个习惯",
]


def check_book(book: str):
    r = {
        "name": book,
        "exists": False,
        "total_slices": 0,
        "note_slices": 0,
        "missing_notes": 0,
        "master_exists": False,
        "master_size": 0,
        "meta_exists": False,
        "meta_status": None,
        "is_complete": False,
        "issues": [],
    }

    d = os.path.join(NOTES_BASE, book)
    if not os.path.isdir(d):
        r["issues"].append("目录不存在")
        return r

    r["exists"] = True
    files = os.listdir(d)

    slices = sorted([f for f in files if re.match(r"^slice_\d+\.md$", f)])
    notes = sorted([f for f in files if re.match(r"^slice_\d+_n\.md$", f)])

    sn = {f.replace("slice_", "").replace(".md", "") for f in slices}
    nn = {f.replace("slice_", "").replace("_n.md", "") for f in notes}

    r["total_slices"] = len(slices)
    r["note_slices"] = len(notes)
    r["missing_notes"] = len(sn - nn)

    master_path = os.path.join(d, "master.md")
    if os.path.exists(master_path):
        r["master_exists"] = True
        r["master_size"] = os.path.getsize(master_path)
    else:
        r["issues"].append("master.md 不存在")

    meta_path = os.path.join(d, "meta.json")
    if os.path.exists(meta_path):
        r["meta_exists"] = True
        try:
            meta = json.loads(open(meta_path, "r", encoding="utf-8").read())
            r["meta_status"] = meta.get("status")
        except Exception:
            r["issues"].append("meta.json 解析失败")
    else:
        r["issues"].append("meta.json 不存在")

    if r["missing_notes"] > 0:
        r["issues"].append(f"缺少 {r['missing_notes']} 个切片笔记")
    if r["master_exists"] and r["master_size"] < 500:
        r["issues"].append("master.md 过小")
    if r["meta_exists"] and r["meta_status"] != "completed":
        r["issues"].append("meta.status 非 completed")

    r["is_complete"] = (
        r["exists"]
        and r["total_slices"] > 0
        and r["missing_notes"] == 0
        and r["master_exists"]
        and r["master_size"] >= 500
        and r["meta_exists"]
        and r["meta_status"] == "completed"
    )

    return r


def main():
    rows = [check_book(b) for b in BOOKS]

    print("=" * 110)
    print(f"{'书名':<22} {'切片':>7} {'笔记':>10} {'缺失':>6} {'master':>10} {'meta':>12} {'状态':>10}")
    print("=" * 110)

    for r in rows:
        master = f"✅{r['master_size']}B" if r["master_exists"] else "❌"
        meta = f"✅{r['meta_status']}" if r["meta_exists"] else "❌"
        status = "✅完成" if r["is_complete"] else "⚠️待修复"
        note_ratio = f"{r['note_slices']}/{r['total_slices']}"
        print(f"{r['name']:<22} {r['total_slices']:>7} {note_ratio:>10} {r['missing_notes']:>6} {master:>10} {meta:>12} {status:>10}")

    print("=" * 110)
    done = sum(1 for r in rows if r["is_complete"])
    print(f"完成：{done}/{len(BOOKS)}")

    pending = [r for r in rows if not r["is_complete"]]
    if pending:
        print("\n待修复明细：")
        for r in pending:
            print(f"- {r['name']}")
            for i in r["issues"]:
                print(f"  - {i}")


if __name__ == "__main__":
    main()
