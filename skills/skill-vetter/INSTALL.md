# Skill Vetter — Installation

> Security-first skill vetting for AI agents. Use before installing any skill from ClawHub, GitHub, or other sources.

---

## For Humans

### Option A: One Command Install (Recommended)

```bash
clawhub install ashanzzz-skill-vetter
```

### Option B: Manual Install

```bash
mkdir -p ~/.openclaw/workspace/skills/skill-vetter
curl -fsSL https://raw.githubusercontent.com/ashanzzz/openclaw-person-skills/main/skills/skill-vetter/SKILL.md \
  -o ~/.openclaw/workspace/skills/skill-vetter/SKILL.md
```

---

## For AI Agents

### Primary Method: Use `clawhub install`

```bash
clawhub install ashanzzz-skill-vetter
```

### Step-by-Step (if clawhub install is unavailable)

> **IMPORTANT: If `clawhub install` is unavailable, use `curl` as fallback.**
> NEVER use WebFetch.

**Step 1: Check if already installed**

```bash
if [ -f "$WORKSPACE/skills/skill-vetter/SKILL.md" ]; then
    echo "Already installed"
    grep "^description:" $WORKSPACE/skills/skill-vetter/SKILL.md | head -1 | cut -c1-80
else
    echo "Not installed"
fi
```

**Step 2: Download SKILL.md**

```bash
mkdir -p ~/.openclaw/workspace/skills/skill-vetter
curl -fsSL https://raw.githubusercontent.com/ashanzzz/openclaw-person-skills/main/skills/skill-vetter/SKILL.md \
  -o ~/.openclaw/workspace/skills/skill-vetter/SKILL.md
```

**Step 3: Verify critical sections**

```bash
for section in "RED FLAGS" "Risk Level" "Vetting Protocol" "Source Check"; do
    grep -qi "$section" $WORKSPACE/skills/skill-vetter/SKILL.md \
      && echo "✓ $section" \
      || echo "✗ MISSING: $section"
done
```

**Step 4: Report to user**

```bash
echo "Skill Vetter installed: $WORKSPACE/skills/skill-vetter/SKILL.md"
echo "Activates on: vetting skills, security checks, before installing from ClawHub/GitHub"
```

---

## Post-Installation

The skill activates when:
- User says: "vet this skill", "check for security issues", "is this safe to install"
- Before installing any skill from ClawHub or GitHub
- Before running unknown code or scripts

## Quick Reference

| Risk Level | Action |
|-----------|--------|
| 🟢 LOW | Basic review, install OK |
| 🟡 MEDIUM | Full code review required |
| 🔴 HIGH | Human approval required |
| ⛔ EXTREME | Do NOT install |

## Uninstall

```bash
clawhub uninstall ashanzzz-skill-vetter
# Or manually:
rm -rf ~/.openclaw/workspace/skills/skill-vetter
```
