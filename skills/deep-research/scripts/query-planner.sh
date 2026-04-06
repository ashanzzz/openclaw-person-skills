#!/usr/bin/env bash
#===========================================================
# query-planner.sh — Generate structured search query plan
#
# Run this BEFORE searching. 
#
# Usage:
#   TOPIC="research topic" [MAX_QUERIES=10] bash query-planner.sh
#
# Output:
#   /tmp/deep-research-cache/{slug}/{ts}/queries/plan.md
#===========================================================

set -e

TOPIC="${TOPIC:?Usage: TOPIC='...' bash query-planner.sh}"
MAX_QUERIES="${MAX_QUERIES:-10}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"

TOPIC_SLUG=$(echo "${TOPIC}" | sed 's/[^a-zA-Z0-9_-]/-/g' | tr '[:upper:]' '[:lower:]' | sed 's/--*/-/g; s/^-//; s/-$//')
if [ -z "${TOPIC_SLUG}" ]; then
    TOPIC_SLUG="topic-$(echo "${TOPIC}" | md5sum | cut -c1-8)"
fi

TIMESTAMP=$(date +%s)
CACHE_DIR="/tmp/deep-research-cache/${TOPIC_SLUG}/${TIMESTAMP}"
QUERIES_DIR="${CACHE_DIR}/queries"
mkdir -p "${QUERIES_DIR}"

echo "query-planner: topic='${TOPIC}'"
echo "query-planner: output='${QUERIES_DIR}'"

NOW=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

python3 - "${TOPIC}" "${QUERIES_DIR}" "${MAX_QUERIES}" "${NOW}" <<'PYEOF'
import json, os, sys, re
from pathlib import Path

topic = sys.argv[1]
queries_dir = sys.argv[2]
max_queries = int(sys.argv[3])
now = sys.argv[4]

os.makedirs(queries_dir, exist_ok=True)

def gen_queries(t, n):
    templates = [
        f'"{t}" official documentation',
        f'"{t}" primary source academic site:arxiv.org OR site:scholar.google.com',
        f'"{t}" latest news 2024 2025',
        f'"{t}" vs comparison review',
        f'"{t}" in-depth analysis technical site:github.com OR site:stackoverflow.com',
        f'"{t}" industry report whitepaper',
        f'"{t}" authoritative guide best practice',
        f'"{t}" controversy OR criticism OR problem limitation',
        f'"{t}" 2025 2026 trend OR prediction OR forecast',
        f'"{t}" alternative OR substitute OR competitor',
    ]
    return templates[:n]

queries = gen_queries(topic, max_queries)

plan_lines = []
plan_lines.append(f"# Query Plan: {topic}")
plan_lines.append(f"")
plan_lines.append(f"**Generated**: {now}")
plan_lines.append(f"**Total queries**: {len(queries)}")
plan_lines.append(f"")
plan_lines.append(f"## Instructions")
plan_lines.append(f"1. Execute each query below in order")
plan_lines.append(f"2. For each key finding → write claim card via claim-card.sh")
plan_lines.append(f"3. After all searches → run manifest.sh → challenge.sh → finalize.sh")
plan_lines.append(f"")
plan_lines.append(f"## Query Plan")
plan_lines.append(f"")

all_queries = []
for i, q in enumerate(queries, 1):
    qid = f"q_{i:03d}"
    all_queries.append({'id': qid, 'query': q, 'status': 'pending'})
    plan_lines.append(f"### {i}. {qid}")
    plan_lines.append(f"- Query: `{q}`")
    plan_lines.append(f"- Status: :hourglass: Pending")
    plan_lines.append(f"- Key dimensions:")
    plan_lines.append(f"- Expected source tier: T1 / T2 / T3")
    plan_lines.append(f"- If significant finding found:")
    plan_lines.append(f"  ```bash")
    plan_lines.append(f"  CLAIM_ID=\"{qid}_claim_001\" CONTENT=\"...\" SOURCE=\"...\" \\")
    plan_lines.append(f"    SOURCE_TIER=\"T2\" VERIFICATION_STATUS=\"pending\" \\")
    plan_lines.append(f"    ROUND=\"1\" CACHE_DIR=\"...\" \\")
    plan_lines.append(f"    bash scripts/claim-card.sh")
    plan_lines.append(f"  ```")
    plan_lines.append(f"")
    
    q_path = Path(queries_dir) / f"{qid}.md"
    q_content = f"""# Query: {q}

**ID**: {qid}
**Status**: :hourglass: Pending
**Research topic**: {topic}

## Execution Log

| Time | Search Executed | Findings |
|------|----------------|----------|
|      |                |          |

## Key Findings
(To be filled after searching)
"""
    q_path.write_text(q_content, encoding='utf-8')

plan_lines.append(f"## Coverage Check")
plan_lines.append(f"- [ ] Factual questions covered (definition/current state)")
plan_lines.append(f"- [ ] Comparative questions covered (vs/alternatives)")
plan_lines.append(f"- [ ] Authoritative sources included (T1/T2)")
plan_lines.append(f"- [ ] Challenge/controversy angles covered")
plan_lines.append(f"- [ ] Time-sensitivity checked (latest news)")
plan_lines.append(f"- [ ] New directions emerged? (if yes → add queries below)")
plan_lines.append(f"")
plan_lines.append(f"## Additional Queries")
plan_lines.append(f"| Query | Direction | Status |")
plan_lines.append(f"|-------|-----------|--------|")
plan_lines.append(f"|       |           | :hourglass: |")

plan_path = Path(queries_dir) / 'plan.md'
plan_path.write_text('\n'.join(plan_lines), encoding='utf-8')

meta = {
    'topic': topic,
    'created_at': now,
    'total_planned': len(queries),
    'queries': all_queries
}
(Path(queries_dir) / 'meta.json').write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding='utf-8')

print(f"query-planner: generated {len(queries)} queries")
print(f"query-planner: open {plan_path}")
PYEOF

echo ""
echo "=== Query Plan Generated ==="
echo "Location: ${QUERIES_DIR}/"
echo "Next: review plan.md, then execute queries"
