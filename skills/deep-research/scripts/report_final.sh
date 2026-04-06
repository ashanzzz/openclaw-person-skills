#!/usr/bin/env bash
#===========================================================
# report_final.sh — Generate final report after user confirms
#
# Run this AFTER user confirms the draft direction.
#
# Usage:
#   CACHE_DIR="..." TOPIC="..." SESSION_ID="..." bash report_final.sh
#
# Output:
#   report_final.md — final polished report
#===========================================================

set -e

CACHE_DIR="${CACHE_DIR:?missing CACHE_DIR}"
TOPIC="${TOPIC:?missing TOPIC}"
SESSION_ID="${SESSION_ID:-unknown}"

DRAFT="${CACHE_DIR}/report_draft.md"
FINAL="${CACHE_DIR}/report_final.md"

if [ ! -f "${DRAFT}" ]; then
    echo "report_final.sh: ERROR — draft not found at ${DRAFT}"
    echo "Please run finalize.sh first to generate the draft."
    exit 1
fi

export CACHE_DIR TOPIC SESSION_ID FINAL DRAFT

python3 - << 'PYEOF'
import json, os, re
from datetime import datetime

cache_dir = os.environ.get('CACHE_DIR', '')
draft_path = os.environ.get('DRAFT', '')
final_path = os.environ.get('FINAL', '')
topic = os.environ.get('TOPIC', '未知主题')
now = datetime.now().strftime('%Y-%m-%d %H:%M UTC')

# Read manifest
with open(os.path.join(cache_dir, 'manifest.json')) as f:
    m = json.load(f)

claims = m.get('claims', [])
tiers = m.get('source_tier_counts', {})
t1, t2, t3, t4 = tiers.get('T1',0), tiers.get('T2',0), tiers.get('T3',0), tiers.get('T4',0)

# Check for challenge dir
challenge_dir = os.path.join(cache_dir, 'challenge')
challenge_done = os.path.exists(challenge_dir)

# Read draft content
with open(draft_path) as f:
    draft = f.read()

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

# Core conclusions (top confidence)
confirmed = sorted(
    [c for c in claims if c.get('verification_status') == 'confirmed'],
    key=conf_score, reverse=True
)[:5]

lines = []
lines.append(f"# 研究报告：{topic}")
lines.append("")
lines.append(f"**日期**：{now.split()[0]}")
lines.append(f"**来源**：{len(claims)} 个（ T1:{t1} / T2:{t2} / T3:{t3} / T4:{t4} ）")
lines.append("")

# Core takeaway
if confirmed:
    best = confirmed[0]
    score = conf_score(best)
    lines.append("## 一句话结论")
    lines.append(f"{conf_label(score)} {best.get('content','')[:300]}")
    lines.append("")

# Key conclusions
lines.append("## 核心结论")
lines.append("")
for i, c in enumerate(confirmed[:5], 1):
    score = conf_score(c)
    label = conf_label(score)
    content = c.get('content', '')
    source = c.get('source', '')
    tier = c.get('source_tier', '')
    deriv = c.get('derivation_chain', '')
    
    lines.append(f"### {i}. {label} {content[:200]}")
    lines.append(f"- **置信度**：{score}/1.0")
    lines.append(f"- **来源**：{source}（{tier}）")
    if deriv:
        lines.append(f"- **推导**：{deriv}")
    if challenge_done:
        lines.append("- **质疑核实**：✅ 已通过对抗性质疑")
    lines.append("")

# Contradicted
contradicted = [c for c in claims if c.get('verification_status') == 'contradicted']
if contradicted:
    lines.append("## ⚠️ 矛盾结论（报告已降权处理）")
    lines.append("")
    for c in contradicted:
        score = conf_score(c)
        label = conf_label(score)
        lines.append(f"- {label} {c.get('content','')[:150]}...")
        lines.append(f"  来源冲突，需人工判断")
    lines.append("")

# User guidance
lines.append("## 对用户的行动建议")
lines.append("")
lines.append("基于以上研究，建议：")
lines.append("1. [具体建议1]")
lines.append("2. [具体建议2]")
lines.append("3. [具体建议3]")
lines.append("")
lines.append("**风险提示**：")
lines.append("- [本次研究中发现的局限性或不确定性]")
lines.append("")

# Sources
lines.append("## 主要参考来源")
seen = set()
for c in claims:
    src = c.get('source', '')
    if src and src not in seen and len(seen) < 15:
        seen.add(src)
        tier = c.get('source_tier', '')
        tier_icon = {'T1':'🟢','T2':'🟡','T3':'⚪','T4':'🔴'}.get(tier,'?')
        lines.append(f"- {tier_icon} {src}")
lines.append("")

lines.append("---")
if challenge_done:
    lines.append(f"*本报告经过对抗性质疑核实。研究缓存：{cache_dir}（保留3天）。*")
else:
    lines.append(f"*注：本次研究未经对抗性质疑流程（可在下次改进）。研究缓存：{cache_dir}（保留3天）。*")

final_content = '\n'.join(lines)
with open(final_path, 'w') as f:
    f.write(final_content)

print(f"report_final.sh: written to {final_path}")
print(f"  Confirmed conclusions: {len(confirmed)}")
print(f"  Contradicted: {len(contradicted)}")
print(f"  Challenge verified: {challenge_done}")
PYEOF

echo ""
echo "=== 最终报告已生成 ==="
echo "文件：${FINAL}"
