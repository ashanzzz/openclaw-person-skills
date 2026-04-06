---
name: deep-research
description: |
  Install: clawhub install deep-research

  Multi-source research methodology. Executes when user asks "研究/调查/搜索" or similar research tasks.
  Supports 3-day research cache + auto-archive to MEMORY.md.
  Provides: 10-step research flow, 4-level source credibility, adversarial challenge, query planning, and user review nodes.
---

# Deep Research 🕵️

A rigorous, multi-source research system with built-in adversarial thinking and user collaboration.

---

## Core Principles

1. **Plan before searching** — Never start blindly; list your queries first
2. **Multi-source cross-verification** — Every key conclusion needs 3 independent sources
3. **Source tiering** — T1/T2 first; T3/T4 only with extra scrutiny
4. **Adversarial thinking** — Actively challenge your own conclusions before reporting
5. **User in the loop** — Report at key milestones so direction can be corrected early
6. **Explicit uncertainty** — Never fabricate; mark every unknown clearly

---

## Research Cache System

### Directory Structure

```
/tmp/deep-research-cache/{topic-slug}/{unix_timestamp}/
  queries/       ← Planned search queries (generated before searching)
  claims/       ← Evidence cards (one per claim)
  rounds/       ← Research round logs
  challenge/    ← Adversarial challenge notes
  manifest.json ← All evidence indexed + statistics
  report_draft.md ← Draft report (before challenge)
  report_final.md ← Final report (after challenge + user review)
  .cleanup_scheduled ← 3-day cleanup marker
```

### 3-Day Cleanup Logic

1. `finalize.sh` writes `.cleanup_scheduled` marker after draft report
2. `cleanup.sh` checks all research dirs on schedule:
   - **Active** (user continued within 3 days) → delete marker, cancel cleanup
   - **Inactive** for >3 days → archive summary to `MEMORY.md`, delete dir
3. `MEMORY.md` content: topic + date + core conclusions + T1/T2/T3/T4 counts + report path (valid until cleanup)

### Continuing Research

User says "继续研究{原话题}" → Agent:
1. Finds latest dir under `/tmp/deep-research-cache/{slug}/`
2. Reads `manifest.json` to see what claims/rounds already exist
3. Continues from where it left off, adding new rounds + claims
4. Updates manifest + re-runs finalize if conclusions changed

---

## Source Credibility (4-Tier)

| Tier | Type | Weight | Rule |
|------|------|--------|------|
| **T1** | Official docs / academic papers / primary data / official APIs | Highest | Use as primary evidence; cite directly |
| **T2** | Authoritative media / industry reports / official announcements | High | Cross-check with T1; use as supporting evidence |
| **T3** | Tech blogs / community discussions / GitHub Issues | Medium | Requires extra verification; use as leads only |
| **T4** | Social media / forums / untraceable citations | Low | Almost never use as evidence; only as leads |

**Rule:** Priority T1 > T2 > T3 > T4. T3/T4 must be validated against T1/T2 before reporting.

---

## Research Flow (10 Steps)

### Step 0: Problem Type Identification

Identify the type before anything else:

| Type | Characteristics | Example |
|------|---------------|---------|
| **Factual** | Has a definite answer | "What is the latest version of XX?" |
| **Comparative** | Needs multi-dimension comparison | "Tool A vs Tool B — which is better?" |
| **Exploratory** | Open-ended, needs synthesis | "What are the market trends for XX?" |
| **Operational** | Needs step-by-step guidance | "How to configure XX on YY?" |

### Step 0.5: Query Planning (BLOCKING — do this BEFORE searching)

**Before touching the web**, generate a structured query plan:

```
[Query Plan]
## Research Questions
1. [Specific question A] → Search queries: ["A exact phrase", "A from T1 source", "A verification"]
2. [Specific question B] → Search queries: [...]
3. ...

## Coverage Check
- Does this query set cover all aspects of the topic? [YES/NO — add if NO]
- Are queries diverse enough (different angles/sources)? [YES/NO — add if NO]
```

**Generate at least 5-8 queries per research topic.** Use the `query-planner.sh` script to help:

```bash
TOPIC="your research topic" bash scripts/query-planner.sh
```

> **Why this matters:** Blind searching leads to confirmation bias. Planning queries first ensures systematic coverage.

### Step 0.75: Time-Sensitivity Check (BLOCKING for AI/tech topics)

For AI / tech / open-source topics:
- Check if any source is older than 6 months
- Mark every piece of evidence with its publication date
- **If a source's age is unknown → downgrade it one tier**

### Step 1: Problem Decomposition

Break the topic into sub-questions aligned with the Query Plan:
- What must be answered?
- What is in scope / out of scope?
- What is the expected output format?
- How many dimensions need to be covered?

### Step 2: Authority Locking

For each sub-question:
- List expected T1/T2 source types
- Identify the most authoritative sources to check first
- Flag if a T1 source is unavailable (note this gap)

### Step 3: Evidence Collection & Claim Cards

For every conclusion found, write a claim card via `claim-card.sh`:

```bash
CLAIM_ID="claim_001" \
CONTENT="specific conclusion..." \
SOURCE="https://..." \
SOURCE_TIER="T2" \
PUBLISHED_AT="2024-03" \
VERIFICATION_STATUS="pending" \
ROUND="1" \
CACHE_DIR="/tmp/deep-research-cache/xxx/xxx" \
bash scripts/claim-card.sh
```

After each research round:
```bash
bash scripts/manifest.sh
```

### Step 4: Build Comparison Framework (for comparative questions)

If comparing things, build a comparison matrix:

| Dimension | Source A | Source B | Source C | Verdict |
|----------|---------|---------|---------|---------|

### Step 5: Reference Alignment & Conflict Resolution

| Situation | Action |
|-----------|--------|
| Multiple sources agree | ✅ Mark verified, elevate confidence |
| Sources conflict | ⚠️ Note each viewpoint, mark as "contradicted pending resolution" |
| Single source only | ⚠️ Mark "single-source — needs 2 more verifications" |

### Step 6: Fact → Conclusion Derivation Chain

Make every derivation explicit:
```
Conclusion X
  ← Based on Fact A (Source: ..., T1, 2024-02) + Fact B (Source: ..., T2, 2023-11)
     Derivation logic: [Explain why A + B → X]
```

### Step 6.5: Adversarial Challenge (BLOCKING — do before draft report)

**Before writing the draft report, actively challenge your own conclusions.**

Create a `challenge/` note for each major conclusion:

```
[Challenge for: Conclusion X]
- What is the weakest part of this conclusion?
- What source could disprove this?
- What would make me abandon this conclusion?
- Is there a plausible alternative explanation?
- Is this conclusion shaped by which sources I happened to find?

Answer each question honestly. If any answer reveals a serious flaw → return to Step 3 to collect more evidence.
```

Use `scripts/challenge.sh` to generate the challenge framework:

```bash
CACHE_DIR="/tmp/deep-research-cache/xxx/xxx" bash scripts/challenge.sh
```

### Step 7: Source Diversity Check

For each major conclusion, assess:
- How many different source domains/立场 contributed? (academia? industry? government? independent?)
- Is the evidence base diverse, or did I just find what I expected to find?
- If sources are homogeneous → flag as "homogeneous evidence — treat as tentative"

Add to the challenge note:
```
Source diversity score: X/Y
  Domains: [list]
  If X < 2: flag as low-diversity, treat conclusion as tentative
```

### Step 8: Draft Report (User Review Node ⭐)

**Before the final report, deliver a draft and ask for user input.**

> "I've completed the research draft. Before I finalize, I want to confirm the direction is right.
>
> **Core findings (3 points):**
> 1. [Finding A] — confidence: 🟢/🟡/🔴
> 2. [Finding B] — confidence: ...
> 3. [Finding C] — confidence: ...
>
> **Key uncertainties:**
> - [Unverified claim]
> - [Conflicting sources on X]
>
> **Does this direction match what you were looking for? Any adjustments before I finalize?**"

This is critical — a 5-minute user check here prevents wasted research in the wrong direction.

### Step 9: Finalize & Deliver

After user confirms (or after reasonable wait):
```bash
bash scripts/finalize.sh
```

Output follows the **Final Report Template** below.

---

## Final Report Template

```markdown
# 研究报告：[Topic]

## 研究概要
- **类型**：[Factual / Comparative / Exploratory / Operational]
- **时间**：[YYYY-MM-DD]
- **来源**：N 个（ T1:N / T2:N / T3:N / T4:N ）
- **核心结论**（1-3句）：

---

## 关键结论

### 结论1：[标题]
- **置信度**：🟢 高 / 🟡 中 / 🔴 低
- **可信度分**：X/Y（来源多样性评分）
- **证据**：
  - [来源A]（T1，2024年）— ...
  - [来源B]（T2，2023年）— ...
- **核实状态**：✅ 已确认 / ⚠️ 待核实 / ❌ 矛盾
- **推导链**：Fact A + Fact B → 结论
- **对用户的意义**：...

### 结论2：（同上）

---

## 存疑项 & 待验证
- ❓ [未核实清楚的点] — 风险：... — 建议：...
- ❓ [发布时间超过6个月的数据] — 建议核实时效性

---

## 对抗性质疑记录
[从 Step 6.5 输出一段：最容易被挑战的点 + 如何处理]

---

## 研究局限性
- [本次未覆盖的范围]
- [方法的局限性]

---

## 主要参考来源
1. [来源名] — [URL] — [T1/T2/T3/T4]
2. ...

---
*本报告经过多源核实 + 对抗性质疑。如有疑问请标注具体结论。*
```

---

## Verification Minimum Requirements

| Evidence Tier | Minimum Verifications |
|-------------|----------------------|
| T1 single source | 2 independent re-checks |
| T2 single source | 2 different sources |
| T1 + T2 multi-source agree | 1 extra check |
| T3 / T4 | **Must upgrade** to T1/T2 or mark "low credibility" |

---

## Scripts Reference

| Script | Purpose |
|--------|---------|
| `research.sh` | Initialize research session + cache dir |
| `query-planner.sh` | Generate structured query plan before searching |
| `claim-card.sh` | Write one evidence card |
| `manifest.sh` | Rebuild manifest.json from all claim cards |
| `challenge.sh` | Generate adversarial challenge framework |
| `finalize.sh` | Generate draft report (triggers user review) |
| `report_final.sh` | Generate final polished report (after user confirms) |
| `cleanup.sh` | 3-day auto-archive check |

### Usage

```bash
# 1. Initialize
TOPIC="research topic" SESSION_ID="optional" bash scripts/research.sh

# 2. Plan queries first (BEFORE searching)
TOPIC="research topic" bash scripts/query-planner.sh

# 3. Search, then record each claim
CLAIM_ID="claim_001" CONTENT="..." SOURCE="..." SOURCE_TIER="T2" \
  PUBLISHED_AT="2024-03" VERIFICATION_STATUS="pending" \
  ROUND="1" CACHE_DIR="..." bash scripts/claim-card.sh

# 4. After each round, update manifest
CACHE_DIR="..." TOPIC="..." SESSION_ID="..." bash scripts/manifest.sh

# 5. Before draft report, run adversarial challenge
CACHE_DIR="..." bash scripts/challenge.sh

# 6. Generate final report
CACHE_DIR="..." TOPIC="..." SESSION_ID="..." bash scripts/finalize.sh
```

---

## Communication Rules

**At research start:**
> "收到。我来系统研究一下。计划：[N]个维度，查找[N]个来源，预计需要[N]步。完成初稿后我会先给你确认方向，再出最终报告。"

**If direction needs adjustment (after draft):**
> "初稿方向是[...]，但我发现[原因]，建议调整为[新方向]，可以吗？"

**At completion:**
> "报告已生成。关于[存疑项]，建议你自己再核实一下[具体点]。报告缓存在[path]，保留3天。"

---

## Self-Improving Integration

After each research, append to `~/.self-improving/domains/research.md`:
```
[YYYY-MM-DD] | Topic: [X] | Sources: N (T1:N T2:N T3:N T4:N) | Quality: 🟢/🟡/🔴 | Lesson: [如果有]
```

If the methodology itself needs improvement → update this SKILL.md.

---

## What Makes This "Perfect" Research

- ✅ Query plan first, searching second
- ✅ User in the loop before final report
- ✅ Adversarial challenge before reporting
- ✅ Explicit derivation chains (no black-box conclusions)
- ✅ Source diversity scored per conclusion
- ✅ Contradictions explicitly marked, not hidden
- ✅ Cache enables continuing research seamlessly
- ✅ 3-day auto-archive keeps MEMORY.md fresh

---

*This skill is inspired by wshuyi/deep-research methodology + arXiv surveys on Deep Research Agents.*
