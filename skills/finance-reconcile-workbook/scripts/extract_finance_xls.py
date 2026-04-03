#!/usr/bin/env python3
"""Extract detail lines from 财务明细 .xls into a normalized CSV.

This script requires `xlrd` (use workspace venv `.venv-xls`).

Output columns:
- sheet, date, month, day, voucher, summary, subject_code, subject_name,
  contra, settle_no, debit, credit, direction, balance

Notes:
- Skips repeated header rows inside sheets.
- Infers year from `--period`.
"""

import argparse
import csv
import re

import xlrd


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--xls", required=True)
    ap.add_argument("--period", required=True, help="YYYYMM, e.g. 202601")
    ap.add_argument("--out", required=True, help="output csv path")
    args = ap.parse_args()

    m = re.match(r"^(\d{4})(\d{2})$", args.period)
    if not m:
        raise SystemExit("--period must be YYYYMM")
    year = int(m.group(1))

    book = xlrd.open_workbook(args.xls)
    rows = []

    for sheet_name in book.sheet_names():
        sh = book.sheet_by_name(sheet_name)
        if sh.nrows < 2:
            continue

        headers = [str(sh.cell_value(0, c)).strip() for c in range(sh.ncols)]
        if "凭证号数" not in headers:
            continue

        idx = {h: i for i, h in enumerate(headers) if h}

        def num(r, col):
            if col is None:
                return 0.0
            v = sh.cell_value(r, col)
            try:
                return float(v)
            except Exception:
                return 0.0

        for r in range(1, sh.nrows):
            # repeated header rows inside sheet
            if str(sh.cell_value(r, idx["凭证号数"])).strip() == "凭证号数":
                continue

            voucher = str(sh.cell_value(r, idx["凭证号数"])).strip()
            if not voucher:
                continue

            month = str(sh.cell_value(r, idx.get("月"))).strip() if "月" in idx else ""
            day = str(sh.cell_value(r, idx.get("日"))).strip() if "日" in idx else ""

            mm = dd = None
            try:
                if month:
                    mm = int(float(month))
                if day:
                    dd = int(float(day))
            except Exception:
                mm = dd = None

            date_str = ""
            if mm and dd:
                date_str = f"{year:04d}-{mm:02d}-{dd:02d}"

            rows.append(
                {
                    "sheet": sheet_name,
                    "date": date_str,
                    "month": mm or "",
                    "day": dd or "",
                    "voucher": voucher,
                    "summary": str(sh.cell_value(r, idx.get("摘要"))).strip() if "摘要" in idx else "",
                    "subject_code": str(sh.cell_value(r, idx.get("科目编码"))).strip() if "科目编码" in idx else "",
                    "subject_name": str(sh.cell_value(r, idx.get("科目名称"))).strip() if "科目名称" in idx else "",
                    "contra": str(sh.cell_value(r, idx.get("对方科目"))).strip() if "对方科目" in idx else "",
                    "settle_no": str(sh.cell_value(r, idx.get("结算号"))).strip() if "结算号" in idx else "",
                    "debit": num(r, idx.get("借方")),
                    "credit": num(r, idx.get("贷方")),
                    "direction": str(sh.cell_value(r, idx.get("方向"))).strip() if "方向" in idx else "",
                    "balance": num(r, idx.get("余额")),
                }
            )

    if not rows:
        raise SystemExit("No rows extracted: check xls format/sheets")

    with open(args.out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)


if __name__ == "__main__":
    main()
