#!/usr/bin/env bash
#===========================================================
# challenge.sh — Adversarial challenge generator
#
# Run this AFTER all research rounds complete and BEFORE
# the draft final report.
#
# Usage:
#   CACHE_DIR="/tmp/deep-research-cache/..." bash challenge.sh
#
# Output:
#   challenge/conclusions.md
#   challenge/challenge_{id}.md
#   challenge/summary.md
#===========================================================

set -e

CACHE_DIR="${CACHE_DIR:?Usage: CACHE_DIR=... bash $0}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
CHALLENGE_DIR="${CACHE_DIR}/challenge"
mkdir -p "${CHALLENGE_DIR}"

echo "challenge.sh: scanning ${CACHE_DIR}"

MANIFEST="${CACHE_DIR}/manifest.json"
if [ ! -f "${MANIFEST}" ]; then
    echo "challenge.sh: manifest.json not found. Run manifest.sh first."
    exit 1
fi

python3 - << 'PYEOF'
import json, os
from pathlib import Path
from datetime import datetime

cache_dir = os.environ.get('CACHE_DIR', '/tmp/deep-research-cache')
challenge_dir = os.path.join(cache_dir, 'challenge')
os.makedirs(challenge_dir, exist_ok=True)

with open(os.path.join(cache_dir, 'manifest.json')) as f:
    manifest = json.load(f)

claims = manifest.get('claims', [])
NOW = datetime.now().strftime('%Y-%m-%d %H:%M UTC')

high_conf = [c for c in claims if c.get('verification_status') == 'confirmed' and c.get('source_tier') in ('T1', 'T2')]
contradicted = [c for c in claims if c.get('verification_status') == 'contradicted']

print(f"Total claims: {len(claims)}, High conf: {len(high_conf)}, Contradicted: {len(contradicted)}")

for i, claim in enumerate(high_conf[:10], 1):
    cid = claim.get('claim_id', f'claim_{i}')
    content = claim.get('content', '')[:200]
    source = claim.get('source', 'unknown')
    tier = claim.get('source_tier', 'T?')
    status = claim.get('verification_status', 'unknown')

    txt = f"""# Adversarial Challenge: {cid}

**Conclusion**: {content}
**Source**: {source} ({tier})
**Status**: {status}

---

## 1. What is the STRONGEST part of this conclusion?
> [Your answer...]

## 2. What is the WEAKEST part?
> [Your answer...]

## 3. What evidence could DISPROVE this?
1.
2.
3.

## 4. Selection bias check
- What search terms did you use? Are they neutral?
- Would the conclusion change with different search terms?
> [Your answer...]

## 5. Alternative explanations not found?
> [List plausible alternatives...]

## 6. Source's own bias
- Industry report? (may favor industry)
- Academic paper? (may have theoretical assumptions)
- Blog? (may have personal bias)
> [Your analysis...]

## 7. Time validity
- When was this conclusion valid?
- Is the field changing fast? (AI typically <6 months)
> [Your analysis...]

## 8. Source diversity score
- How many different domains contributed?
- Homogeneous sources → downgrade confidence

---

## Response

| Challenge Point | Valid? | How to Address |
|----------------|--------|----------------|
|                |        |                |

## Final Judgment
- [ ] Withstands challenge → Keep in report
- [ ] Has flaws → Return to Step 3
- [ ] Needs qualification → Add scope limits in report

**Confidence adjustment**: [original] → [post-challenge]
"""
    (Path(challenge_dir) / f"challenge_{cid}.md").write_text(txt, encoding='utf-8')
    print(f"  Generated: challenge_{cid}.md")

# Conclusions list
lines = [f"# Conclusions to Challenge\nGenerated: {NOW}\n\n"]
for i, c in enumerate(high_conf[:10], 1):
    lines.append(f"{i}. **{c.get('claim_id','?')}** — {c.get('content','')[:80]}...")
    lines.append(f"   Source: {c.get('source','?')} ({c.get('source_tier','T?')})\n")
if contradicted:
    lines.append("\n## ⚠️ Contradicted (handle first)\n")
    for c in contradicted:
        lines.append(f"- {c.get('claim_id','?')}: {c.get('content','')[:60]}...\n")
(Path(challenge_dir) / 'conclusions.md').write_text(''.join(lines), encoding='utf-8')
print("  Generated: conclusions.md")

# Summary
summary = f"""# Challenge Summary

Generated: {NOW}
Dir: {cache_dir}
High-conf claims: {len(high_conf[:10])}
Contradicted: {len(contradicted)}

## Status
- [x] Read manifest
- [x] Generate conclusions list
- [ ] Complete all challenges
- [ ] Integrate results
- [ ] Adjust confidence levels

## Priority

| Priority | Claim | Issue | Status |
|----------|-------|-------|--------|
| 🔴 High |        |       | Pending |
| 🟡 Medium |        |       | Pending |
| 🟢 Low |        |       | Pending |

## Next Steps
After completing all challenges:
1. Keep conclusions that withstand challenge
2. Add scope qualifications where needed
3. Remove or redo flawed conclusions
"""
(Path(challenge_dir) / 'summary.md').write_text(summary, encoding='utf-8')
print("  Generated: summary.md")
print(f"\nchallenge.sh: COMPLETE — open {challenge_dir}/summary.md")
PYEOF

echo ""
echo "=== Adversarial Challenge Complete ==="
echo "Location: ${CHALLENGE_DIR}/"
echo "Next: open conclusions.md, handle each challenge file"
