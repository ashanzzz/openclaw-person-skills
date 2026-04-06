#!/usr/bin/env bash
#===========================================================
# finalize.sh — Generate draft report + schedule cleanup
#
# This generates a DRAFT report FIRST (report_draft.md),
# then waits for user review before generating report_final.md.
#
# Usage:
#   CACHE_DIR="..." TOPIC="..." SESSION_ID="..." bash finalize.sh
#
# Output:
#   report_draft.md    — draft for user review
#   .cleanup_scheduled — 3-day cleanup marker
#===========================================================

set -e

CACHE_DIR="${CACHE_DIR:?missing CACHE_DIR}"
TOPIC="${TOPIC:?missing TOPIC}"
SESSION_ID="${SESSION_ID:-unknown}"

MANIFEST_PATH="${CACHE_DIR}/manifest.json"
DRAFT_PATH="${CACHE_DIR}/report_draft.md"

export CACHE_DIR MANIFEST_PATH DRAFT_PATH TOPIC SESSION_ID

python3 - << 'PYEOF'
import json, os, re
from datetime import datetime

manifest_path = os.environ.get('MANIFEST_PATH', '')
draft_path = os.environ.get('DRAFT_PATH', '')
topic = os.environ.get('TOPIC', '未知主题')
cache_dir = os.environ.get('CACHE_DIR', '')
now = datetime.now().strftime('%Y-%m-%d %H:%M UTC')

if not os.path.exists(manifest_path):
    print(f"finalize: ERROR — manifest.json not found")
    exit(1)

with open(manifest_path) as f:
    m = json.load(f)

claims = m.get('claims', [])
tiers = m.get('source_tier_counts', {})
t1, t2, t3, t4 = tiers.get('T1',0), tiers.get('T2',0), tiers.get('T3',0), tiers.get('T4',0)
total = len(claims)

# Categorize
confirmed = [c for c in claims if c.get('verification_status') == 'confirmed']
pending = [c for c in claims if c.get('verification_status') not in ('confirmed', 'contradicted')]
contradicted = [c for c in claims if c.get('verification_status') == 'contradicted']

# Confidence scoring
def conf_score(claim):
    tier = claim.get('source_tier', 'T4')
    status = claim.get('verification_status', 'pending')
    base = {'T1': 1.0, 'T2': 0.85, 'T3': 0.6, 'T4': 0.3}.get(tier, 0.3)
    if status == 'confirmed': mult = 1.0
    elif status == 'verified': mult = 1.0
    elif status == 'contradicted': mult = 0.2
    else: mult = 0.6
    return round(base * mult, 2)

def conf_label(score):
    if score >= 0.8: return '🟢'
    elif score >= 0.5: return '🟡'
    else: return '🔴'

# Check for challenge dir
challenge_dir = os.path.join(cache_dir, 'challenge')
challenge_exists = os.path.exists(challenge_dir)
challenge_notes = []
if challenge_exists:
    for f in os.listdir(challenge_dir):
        if f.startswith('challenge_') and f.endswith('.md'):
            cid = f.replace('challenge_','').replace('.md','')
            challenge_notes.append(cid)

lines = []
lines.append(f"# 研究报告（草稿）：{topic}")
lines.append("")
lines.append(f"**生成时间**：{now}")
lines.append(f"**状态**：📝 草稿 — 请审核后确认最终版本")
lines.append("")
lines.append("## 研究概要")
lines.append(f"- **研究主题**：{topic}")
lines.append(f"- **来源总数**：{total} 个")
lines.append(f"  - T1（官方/学术/一手）：{t1} 个")
lines.append(f"  - T2（权威媒体/行业）：{t2} 个")
lines.append(f"  - T3（技术博客/社区）：{t3} 个")
lines.append(f"  - T4（社媒/无法溯源）：{t4} 个")
lines.append(f"- **已确认**：{len(confirmed)} | **待核实**：{len(pending)} | **矛盾**：{len(contradicted)}")
if challenge_exists:
    lines.append(f"- **已完成对抗性质疑**：{len(challenge_notes)} 个结论")
lines.append("")
lines.append("## 关键结论")
lines.append("")
for i, c in enumerate(confirmed[:8], 1):
    score = conf_score(c)
    label = conf_label(score)
    content = c.get('content', '')[:300]
    source = c.get('source', 'unknown')
    tier = c.get('source_tier', 'T?')
    verified_by = c.get('verified_by', [])
    deriv = c.get('derivation_chain', '')
    
    lines.append(f"### {label} 结论{i}：{c.get('claim_id','?')}")
    lines.append(f"- **置信度**：{score}/1.0 {label}")
    lines.append(f"- **内容**：{content}")
    lines.append(f"- **来源**：{source}（{tier}）")
    if verified_by:
        lines.append(f"- **核实来源**：{', '.join(str(v) for v in verified_by[:2])}")
    if deriv:
        lines.append(f"- **推导链**：{deriv}")
    if c.get('claim_id','') in challenge_notes:
        lines.append(f"- **对抗性核实**：✅ 已通过")
    lines.append("")

if contradicted:
    lines.append("## ⚠️ 矛盾结论（需优先处理）")
    lines.append("")
    for c in contradicted:
        score = conf_score(c)
        label = conf_label(score)
        content = c.get('content', '')[:200]
        lines.append(f"- {label} **{c.get('claim_id','?')}**: {content}")
        lines.append(f"  来源：{c.get('source','?')} — 需人工裁决")
    lines.append("")

if pending:
    lines.append("## ⏳ 待核实结论")
    lines.append("")
    for c in pending[:5]:
        lines.append(f"- **{c.get('claim_id','?')}**: {c.get('content','')[:100]}...")
        lines.append(f"  来源：{c.get('source','?')}（{c.get('source_tier','T?')}）")
    if len(pending) > 5:
        lines.append(f"- ...还有 {len(pending)-5} 条")
    lines.append("")

lines.append("## 来源分布")
lines.append(f"| 可信度 | 数量 |")
lines.append(f"|---------|------|")
lines.append(f"| 🟢 T1 官方/学术/一手 | {t1} |")
lines.append(f"| 🟡 T2 权威媒体/行业报告 | {t2} |")
lines.append(f"| ⚪ T3 技术博客/社区 | {t3} |")
lines.append(f"| 🔴 T4 社媒/无法溯源 | {t4} |")
lines.append("")

# Evidence table
if claims:
    lines.append("## 完整证据卡")
    lines.append(f"| # | 结论ID | 可信度 | 状态 | 来源 |")
    lines.append(f"|---|--------|--------|------|------|")
    for i, c in enumerate(claims, 1):
        score = conf_score(c)
        label = conf_label(score)
        cid = c.get('claim_id','')
        tier = c.get('source_tier','')
        status = c.get('verification_status','')
        src = re.sub(r'https?://', '', c.get('source','?'))[:35]
        status_icon = {'confirmed':'✅','verified':'✅','pending':'⏳','contradicted':'❌'}.get(status,'❓')
        lines.append(f"| {i} | {cid} | {label}{score} | {status_icon}{status} | {src} |")
    lines.append("")

# Limitations
lines.append("## 研究局限性")
lines.append("- 本次未覆盖的范围：")
lines.append("- 方法论的局限：")
lines.append("- 来源偏差说明：")
lines.append("")

lines.append("---")
lines.append(f"*本报告为草稿，请审核方向是否正确后再确认生成最终版本。*")
lines.append(f"*生成时间：{now} | 缓存保留3天*")

content = '\n'.join(lines)
with open(draft_path, 'w') as f:
    f.write(content)

print(f"finalize: draft written to {draft_path}")
print(f"  Claims: {total} | T1:{t1} T2:{t2} T3:{t3} T4:{t4}")
print(f"  Confirmed: {len(confirmed)} | Pending: {len(pending)} | Contradicted: {len(contradicted)}")
PYEOF

# Schedule cleanup
SLUG=$(echo "${TOPIC}" | sed 's/[^a-zA-Z0-9_-]/-/g' | tr '[:upper:]' '[:lower:]' | sed 's/--*/-/g; s/^-//; s/-$//')
if [ -z "${SLUG}" ]; then SLUG="topic-$(echo "${TOPIC}" | md5sum | cut -c1-8)"; fi
MARKER_DIR="/tmp/deep-research-cache/${SLUG}"
MARKER_FILE="${MARKER_DIR}/.cleanup_scheduled"
mkdir -p "${MARKER_DIR}"
SCHEDULED=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
echo "{\"scheduled_at\":\"${SCHEDULED}\",\"draft_path\":\"${DRAFT_PATH}\",\"session_id\":\"${SESSION_ID}\",\"topic\":\"${TOPIC}\"}" > "${MARKER_FILE}"

echo ""
echo "=== 草稿报告已生成 ==="
echo "文件：${DRAFT_PATH}"
echo ""
echo "【请先审核草稿，确认方向正确后回复"确认"或"可以" → 我将生成最终版本】"
echo ""
echo "草稿摘要："
head -25 "${DRAFT_PATH}"
