#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Export ERPNext invoices for a company + month.

- Reads ERP_BASE_URL + ERP_API_TOKEN from secure/erpnext/qifu.env by default.
- Exports list to CSV/JSON and writes a markdown summary.
- Optionally downloads PDFs.

Safe-by-default:
- Never prints the API token.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import os
import re
import sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Tuple

import requests

DEFAULT_ENV_PATH = "/root/.openclaw/workspace/secure/api-fillin.env"
DEFAULT_OUT_ROOT = "/root/.openclaw/workspace/secure/erpnext/exports"


def parse_env_file(path: str) -> Dict[str, str]:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"env file not found: {path}")
    out: Dict[str, str] = {}
    for raw in p.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        out[k.strip()] = v.strip()
    return out


def month_range(month: str) -> Tuple[str, str]:
    # month: YYYY-MM
    m = re.fullmatch(r"(\d{4})-(\d{2})", month)
    if not m:
        raise ValueError("--month must be YYYY-MM")
    y = int(m.group(1))
    mo = int(m.group(2))
    start = dt.date(y, mo, 1)
    if mo == 12:
        end = dt.date(y + 1, 1, 1) - dt.timedelta(days=1)
    else:
        end = dt.date(y, mo + 1, 1) - dt.timedelta(days=1)
    return start.isoformat(), end.isoformat()


def slug(s: str) -> str:
    s = s.strip()
    s = re.sub(r"\s+", "_", s)
    s = re.sub(r"[^0-9A-Za-z_\-\u4e00-\u9fff]", "", s)
    return s[:80] or "_"


def erp_list(
    base_url: str,
    token: str,
    doctype: str,
    fields: List[str],
    filters: List[Any],
    page_len: int = 200,
) -> List[Dict[str, Any]]:
    base = base_url.rstrip("/")
    url = f"{base}/api/resource/{requests.utils.quote(doctype)}"
    headers = {"Authorization": f"token {token}"}
    out: List[Dict[str, Any]] = []
    start = 0
    while True:
        params = {
            "fields": json.dumps(fields, ensure_ascii=False),
            "filters": json.dumps(filters, ensure_ascii=False),
            "limit_start": start,
            "limit_page_length": page_len,
        }
        r = requests.get(url, headers=headers, params=params, timeout=30)
        if r.status_code == 401:
            raise PermissionError("ERP API returned 401 (token invalid)")
        r.raise_for_status()
        data = r.json().get("data") or []
        if not data:
            break
        out.extend(data)
        if len(data) < page_len:
            break
        start += page_len
    return out


def download_pdf(base_url: str, token: str, doctype: str, name: str) -> bytes:
    base = base_url.rstrip("/")
    url = f"{base}/api/method/frappe.utils.print_format.download_pdf"
    headers = {"Authorization": f"token {token}"}
    params = {
        "doctype": doctype,
        "name": name,
        # let server choose default print format
    }
    r = requests.get(url, headers=headers, params=params, timeout=60)
    if r.status_code == 401:
        raise PermissionError("ERP API returned 401 (token invalid)")
    r.raise_for_status()
    return r.content


def write_csv(path: Path, rows: List[Dict[str, Any]], fields: List[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for row in rows:
            w.writerow({k: row.get(k, "") for k in fields})


def safe_float(x: Any) -> float:
    try:
        return float(x)
    except Exception:
        return 0.0


def _is_no_invoice_bill_no(bill_no: Any) -> bool:
    """User rule: bill_no == '0' or continuous zeros => 无票支出.

    Also treats empty/None as no-invoice (practically common)."""
    if bill_no is None:
        return True
    s = str(bill_no).strip()
    if s == "":
        return True
    # normalize common separators/spaces
    s2 = re.sub(r"\s+", "", s)
    if re.fullmatch(r"0+", s2):
        return True
    return False


def build_summary(
    doctype: str,
    month: str,
    company: str,
    rows: List[Dict[str, Any]],
    key_party_field: str,
    pdf_stats: Dict[str, str] | None = None,
) -> str:
    statuses = defaultdict(int)
    by_party_total = defaultdict(float)
    by_party_outstanding = defaultdict(float)

    total_grand = 0.0
    total_outstanding = 0.0

    noinv_count = 0
    noinv_total = 0.0

    for r in rows:
        st = str(r.get("status", ""))
        statuses[st] += 1
        party = str(r.get(key_party_field, ""))
        grand = safe_float(r.get("grand_total"))
        out = safe_float(r.get("outstanding_amount"))
        total_grand += grand
        total_outstanding += out
        if party:
            by_party_total[party] += grand
            by_party_outstanding[party] += out

        if _is_no_invoice_bill_no(r.get("bill_no")):
            noinv_count += 1
            noinv_total += grand

    top_total = sorted(by_party_total.items(), key=lambda kv: kv[1], reverse=True)[:15]
    top_out = sorted(by_party_outstanding.items(), key=lambda kv: kv[1], reverse=True)[:15]

    lines = []
    lines.append(f"# ERPNext 发票导出汇总\n\n")
    lines.append(f"- Doctype: **{doctype}**\n")
    lines.append(f"- Company: **{company}**\n")
    lines.append(f"- Month: **{month}**\n")
    lines.append(f"- Count: **{len(rows)}**\n")
    lines.append(f"- Total (grand_total): **{total_grand:.2f}**\n")
    lines.append(f"- Total (outstanding_amount): **{total_outstanding:.2f}**\n")
    lines.append(f"- 无票支出（bill_no 为空 / 0 / 全0）：**{noinv_count}** 单，合计 **{noinv_total:.2f}**\n\n")

    lines.append("## Status 统计\n")
    for st, n in sorted(statuses.items(), key=lambda kv: (-kv[1], kv[0])):
        lines.append(f"- {st or '(empty)'}: {n}\n")

    lines.append("\n## Top 供应商/客户（按金额）\n")
    for name, val in top_total:
        lines.append(f"- {name}: {val:.2f}\n")

    lines.append("\n## Top 供应商/客户（按未结清金额 outstanding）\n")
    for name, val in top_out:
        lines.append(f"- {name}: {val:.2f}\n")

    if pdf_stats:
        ok = sum(1 for v in pdf_stats.values() if v == "ok")
        fail = len(pdf_stats) - ok
        lines.append("\n## PDF 下载\n")
        lines.append(f"- ok: {ok}\n- fail: {fail}\n")
        if fail:
            lines.append("\n失败明细（name -> reason）：\n")
            for k, v in list(pdf_stats.items()):
                if v != "ok":
                    lines.append(f"- {k}: {v}\n")

    return "".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--env", default=DEFAULT_ENV_PATH)
    ap.add_argument("--out-root", default=DEFAULT_OUT_ROOT)
    ap.add_argument("--company", required=True)
    ap.add_argument("--month", required=True, help="YYYY-MM")
    ap.add_argument("--doctype", default="Purchase Invoice", choices=["Purchase Invoice", "Sales Invoice"])
    ap.add_argument("--include-draft", action="store_true", help="include docstatus=0")
    ap.add_argument("--pdf", action="store_true", help="download each invoice pdf")
    args = ap.parse_args()

    env = parse_env_file(args.env)
    base_url = env.get("ERP_BASE_URL")
    token = env.get("ERP_API_TOKEN")
    if not base_url or not token:
        raise RuntimeError("ERP_BASE_URL / ERP_API_TOKEN missing in env")

    start, end = month_range(args.month)
    company = args.company
    doctype = args.doctype

    # doctype-specific fields
    if doctype == "Purchase Invoice":
        party_field = "supplier"
        fields = [
            "name",
            "posting_date",
            "company",
            "supplier",
            "supplier_name",
            # Supplier Invoice No (常用于“发票号/供应商票号”口径)
            "bill_no",
            "bill_date",
            "grand_total",
            "outstanding_amount",
            "status",
        ]
    else:
        party_field = "customer"
        fields = [
            "name",
            "posting_date",
            "company",
            "customer",
            "customer_name",
            # Customer invoice ref (销售侧可能不同；先沿用 bill_no)
            "bill_no",
            "bill_date",
            "grand_total",
            "outstanding_amount",
            "status",
        ]

    filters: List[Any] = [
        ["posting_date", "between", [start, end]],
        ["company", "=", company],
    ]
    if args.include_draft:
        filters.append(["docstatus", "in", [0, 1]])
    else:
        filters.append(["docstatus", "=", 1])

    rows = erp_list(base_url, token, doctype, fields, filters)

    out_dir = Path(args.out_root) / slug(company) / args.month
    out_dir.mkdir(parents=True, exist_ok=True)

    csv_path = out_dir / f"invoices_{slug(doctype)}_{args.month}.csv"
    json_path = out_dir / f"invoices_{slug(doctype)}_{args.month}.json"
    summary_path = out_dir / f"summary_{slug(doctype)}_{args.month}.md"

    # split: 无票支出（bill_no 为空/0/全0）
    noinv_csv_path = out_dir / f"no_invoice_{slug(doctype)}_{args.month}.csv"

    write_csv(csv_path, rows, fields)
    json_path.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")

    noinv_rows = [r for r in rows if _is_no_invoice_bill_no(r.get('bill_no'))]
    write_csv(noinv_csv_path, noinv_rows, fields)

    pdf_stats: Dict[str, str] | None = None
    if args.pdf:
        pdf_stats = {}
        pdf_dir = out_dir / "pdf"
        pdf_dir.mkdir(parents=True, exist_ok=True)
        for r in rows:
            name = str(r.get("name"))
            if not name:
                continue
            try:
                content = download_pdf(base_url, token, doctype, name)
                (pdf_dir / f"{name}.pdf").write_bytes(content)
                pdf_stats[name] = "ok"
            except Exception as e:
                pdf_stats[name] = f"{type(e).__name__}: {str(e)[:120]}"

    summary = build_summary(doctype, args.month, company, rows, party_field, pdf_stats=pdf_stats)
    summary_path.write_text(summary, encoding="utf-8")

    print(str(out_dir))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except PermissionError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        print(f"Fix: update ERP_API_TOKEN in {DEFAULT_ENV_PATH} (do not paste it into chat).", file=sys.stderr)
        raise
