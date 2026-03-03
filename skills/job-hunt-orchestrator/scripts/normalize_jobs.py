#!/usr/bin/env python3
import json
import re
import sys


def normalize_text(text):
    if text is None:
        return ""
    return re.sub(r"\s+", " ", str(text)).strip()


def key_of(item):
    company = normalize_text(item.get("company", "")).lower()
    title = normalize_text(item.get("position_title", "")).lower()
    url = normalize_text(item.get("official_job_url", "")).lower()
    return (company, title, url)


def main():
    if len(sys.argv) < 3:
        print("Usage: normalize_jobs.py input.json output.json")
        sys.exit(1)

    with open(sys.argv[1], "r", encoding="utf-8") as file:
        records = json.load(file)

    seen = set()
    result = []

    for record in records:
        normalized = dict(record)
        for field in [
            "company",
            "position_title",
            "location",
            "source_url",
            "official_job_url",
            "apply_url",
            "salary",
            "requirements_summary",
            "responsibilities_summary",
            "laborlaw_signals",
            "fit_reason",
        ]:
            normalized[field] = normalize_text(normalized.get(field, ""))

        duplicate_key = key_of(normalized)
        if duplicate_key in seen:
            continue
        seen.add(duplicate_key)
        result.append(normalized)

    with open(sys.argv[2], "w", encoding="utf-8") as file:
        json.dump(result, file, ensure_ascii=False, indent=2)

    print(f"normalized={len(result)}")


if __name__ == "__main__":
    main()
