#!/usr/bin/env python3
import json
import sys


def has_value(value):
    return value is not None and str(value).strip() != ""


def score(record):
    total = 0

    # 1) 区域匹配 25
    distance = record.get("distance_km")
    if isinstance(distance, (int, float)) and distance <= 30:
        total += 25
    elif isinstance(distance, (int, float)) and distance <= 50:
        total += 12

    # 2) 岗位匹配 25（由上游标注 keyword_match 0~25）
    total += int(record.get("keyword_match", 0))
    if total > 100:
        total = 100

    # 3) 外企质量 20
    if record.get("source_type") in ["official_site", "official_ats"]:
        total += 20

    # 4) 劳动法友好 20
    level = str(record.get("labor_law_score", "")).lower()
    if level == "high":
        total += 20
    elif level == "medium":
        total += 10

    # 5) 薪资透明 10
    salary = str(record.get("salary", "")).strip()
    if salary and salary != "未公开":
        total += 10

    if total > 100:
        total = 100

    official = has_value(record.get("official_job_url"))
    apply = has_value(record.get("apply_url"))
    posted = has_value(record.get("posted_date"))

    if not official or not apply or not posted:
        bucket = "verify_needed"
    elif total >= 75:
        bucket = "apply_now"
    else:
        bucket = "watchlist"

    return total, bucket


def main():
    if len(sys.argv) < 3:
        print("Usage: score_jobs.py input.json output.json")
        sys.exit(1)

    with open(sys.argv[1], "r", encoding="utf-8") as file:
        records = json.load(file)

    for record in records:
        fit_score, bucket = score(record)
        record["fit_score"] = fit_score
        record["bucket"] = bucket

    with open(sys.argv[2], "w", encoding="utf-8") as file:
        json.dump(records, file, ensure_ascii=False, indent=2)

    print(f"scored={len(records)}")


if __name__ == "__main__":
    main()
