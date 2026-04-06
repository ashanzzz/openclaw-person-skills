# Skill Vetter — Installation Guide

> Security-first skill vetting for AI agents. Use before installing any skill from ClawHub, GitHub, or other sources.

---

## For Humans

### Option A: Let an AI Agent Do It (Recommended)

Copy and paste this into your AI agent (OpenClaw, Claude Code, Cursor, etc.):

```
Install and configure the Skill Vetter skill by following the instructions here:
https://raw.githubusercontent.com/ashanzzz/openclaw-person-skills/main/skills/skill-vetter/INSTALL.md
```

### Option B: Manual Installation

**Step 1:** Create the skills directory:

```bash
mkdir -p ~/.openclaw/workspace/skills/skill-vetter
```

**Step 2:** Download the SKILL.md:

```bash
curl -fsSL https://raw.githubusercontent.com/ashanzzz/openclaw-person-skills/main/skills/skill-vetter/SKILL.md \
  -o ~/.openclaw/workspace/skills/skill-vetter/SKILL.md
```

**Step 3:** Verify:

```bash
head -10 ~/.openclaw/workspace/skills/skill-vetter/SKILL.md
```

---

## For AI Agents

> **IMPORTANT: Use `curl` to fetch this file, NOT WebFetch or web_fetch.**
> Always use:
> ```bash
> curl -fsSL https://raw.githubusercontent.com/ashanzzz/openclaw-person-skills/main/skills/skill-vetter/INSTALL.md
> ```

### Step 1: Detect Existing Installation

```bash
if [ -f "$WORKSPACE/skills/skill-vetter/SKILL.md" ]; then
    echo "Already installed"
    grep "^description:" $WORKSPACE/skills/skill-vetter/SKILL.md | head -1
else
    echo "Not installed"
fi
```

### Step 2: Create Directory

```bash
mkdir -p ~/.openclaw/workspace/skills/skill-vetter
```

### Step 3: Download SKILL.md

```bash
curl -fsSL https://raw.githubusercontent.com/ashanzzz/openclaw-person-skills/main/skills/skill-vetter/SKILL.md \
  -o ~/.openclaw/workspace/skills/skill-vetter/SKILL.md
```

### Step 4: Verify Content

```bash
# Verify critical sections exist
for section in "RED FLAGS" "Risk Level" "Vetting Protocol" "Source Check"; do
    if grep -qi "$section" $WORKSPACE/skills/skill-vetter/SKILL.md; then
        echo "✓ Found: $section"
    else
        echo "✗ MISSING: $section"
    fi
done
```

### Step 5: Report to User

```bash
echo "Skill Vetter installed at: $WORKSPACE/skills/skill-vetter/SKILL.md"
echo "Activated when: vetting a skill, checking for red flags, before installing from ClawHub/GitHub"
```

---

## Post-Installation

After installing, the skill activates when:
- Installing any skill from ClawHub or GitHub
- User says: "vet this skill", "check for security issues", "is this safe to install"
- Before running any unknown code or scripts

The skill performs: Source check, Code review (RED FLAGS scan), Permission scope analysis, Risk classification (LOW / MEDIUM / HIGH / EXTREME).

## Skill Vetter Quick Reference

| Risk Level | Action |
|-----------|--------|
| 🟢 LOW | Basic review, install OK |
| 🟡 MEDIUM | Full code review required |
| 🔴 HIGH | Human approval required |
| ⛔ EXTREME | Do NOT install |
