#!/usr/bin/env bash
#===========================================================
# research.sh — Initialize a new research session
#
# Usage:
#   TOPIC="research topic" SESSION_ID="optional" bash research.sh
#
# What it does:
#   1. Creates cache directory structure
#   2. Writes metadata
#   3. Prints next-step instructions
#===========================================================

set -e

TOPIC="${TOPIC:?Usage: TOPIC='...' bash research.sh}"
SESSION_ID="${SESSION_ID:-$(date +%s)}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
SKILL_DIRNAME="$(basename "${SKILL_DIR}")"

# Create cache structure
SLUG=$(echo "${TOPIC}" | sed 's/[^a-zA-Z0-9_-]/-/g' | tr '[:upper:]' '[:lower:]' | sed 's/--*/-/g; s/^-//; s/-$//')
if [ -z "${SLUG}" ]; then SLUG="topic-$(echo "${TOPIC}" | md5sum | cut -c1-8)"; fi

TIMESTAMP=$(date +%s)
CACHE_DIR="/tmp/deep-research-cache/${SLUG}/${TIMESTAMP}"

mkdir -p "${CACHE_DIR}"/{queries,claims,rounds,challenge}
echo "=== Deep Research Started ==="
echo "Topic: ${TOPIC}"
echo "Slug: ${SLUG}"
echo "Session: ${SESSION_ID}"
echo "Cache: ${CACHE_DIR}"

# Write metadata
cat > "${CACHE_DIR}/metadata.json" << METADEOF
{
  "topic": "${TOPIC}",
  "slug": "${SLUG}",
  "session_id": "${SESSION_ID}",
  "started_at": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "status": "active",
  "query_plan_generated": false,
  "rounds_completed": 0,
  "claims_recorded": 0,
  "challenge_completed": false,
  "draft_generated": false,
  "final_generated": false,
  "cache_expires_at": "$(date -u -d '+3 days' +"%Y-%m-%dT%H:%M:%SZ" 2>/dev/null || date -v+3d -u +"%Y-%m-%dT%H:%M:%SZ")"
}
METADEOF

echo ""
echo "=== Cache initialized ==="
echo ""
echo "下一步操作顺序（请严格按顺序执行）："
echo ""
echo "1. 【生成查询计划 — 在搜索前必须做！】"
echo "   TOPIC=\"${TOPIC}\" bash ${SKILL_DIRNAME}/scripts/query-planner.sh"
echo ""
echo "2. 打开 queries/plan.md 查看查询计划"
echo ""
echo "3. 按计划执行搜索，每找到一个关键结论："
echo "   CLAIM_ID=\"q_001_claim_001\" \\"
echo "   CONTENT=\"具体结论内容\" \\"
echo "   SOURCE=\"https://...\" \\"
echo "   SOURCE_TIER=\"T2\" \\"
echo "   PUBLISHED_AT=\"2024-03\" \\"
echo "   VERIFICATION_STATUS=\"pending\" \\"
echo "   ROUND=\"1\" \\"
echo "   CACHE_DIR=\"${CACHE_DIR}\" \\"
echo "   bash ${SKILL_DIRNAME}/scripts/claim-card.sh"
echo ""
echo "4. 每轮搜索结束后："
echo "   CACHE_DIR=\"${CACHE_DIR}\" TOPIC=\"${TOPIC}\" SESSION_ID=\"${SESSION_ID}\" \\"
echo "   bash ${SKILL_DIRNAME}/scripts/manifest.sh"
echo ""
echo "5. 全部结论收集完毕后（在写草稿前）："
echo "   CACHE_DIR=\"${CACHE_DIR}\" bash ${SKILL_DIRNAME}/scripts/challenge.sh"
echo ""
echo "6. 生成草稿报告（含用户Review节点）："
echo "   CACHE_DIR=\"${CACHE_DIR}\" TOPIC=\"${TOPIC}\" SESSION_ID=\"${SESSION_ID}\" \\"
echo "   bash ${SKILL_DIRNAME}/scripts/finalize.sh"
echo ""
echo "7. 用户确认草稿后，生成最终报告："
echo "   CACHE_DIR=\"${CACHE_DIR}\" TOPIC=\"${TOPIC}\" SESSION_ID=\"${SESSION_ID}\" \\"
echo "   bash ${SKILL_DIRNAME}/scripts/report_final.sh"
echo ""
echo "=== 开始吧！先做 Step 0.5：生成查询计划 ==="
