# Deep Research Skill — Installation

---

## For Humans

### Option A: One Command Install (Recommended)

```bash
clawhub install ashanzzz-deep-research
```

That's it. Your AI agent will download and install the skill automatically.

### Option B: Manual Install

If you prefer to do it yourself:

```bash
# Create the skills directory
mkdir -p ~/.openclaw/workspace/skills/deep-research

# Download the SKILL.md
curl -fsSL https://raw.githubusercontent.com/ashanzzz/openclaw-person-skills/main/skills/deep-research/SKILL.md \
  -o ~/.openclaw/workspace/skills/deep-research/SKILL.md

# Verify
head -20 ~/.openclaw/workspace/skills/deep-research/SKILL.md
```

---

## For AI Agents

### Primary Method: Use `clawhub install`

```bash
clawhub install ashanzzz-deep-research
```

### Step-by-Step (if clawhub install is unavailable)

> **IMPORTANT: If `clawhub install` is unavailable, use `curl` as fallback.**
> NEVER use WebFetch — it summarizes content and strips formatting.

**Step 1: Check if already installed**

```bash
if [ -f "$WORKSPACE/skills/deep-research/SKILL.md" ]; then
    echo "Already installed: $WORKSPACE/skills/deep-research/SKILL.md"
    grep "^version:" $WORKSPACE/skills/deep-research/SKILL.md | head -1
else
    echo "Not installed"
fi
```

**Step 2: Download via curl**

```bash
mkdir -p ~/.openclaw/workspace/skills/deep-research
curl -fsSL https://raw.githubusercontent.com/ashanzzz/openclaw-person-skills/main/skills/deep-research/SKILL.md \
  -o ~/.openclaw/workspace/skills/deep-research/SKILL.md
```

**Step 3: Verify integrity**

```bash
for section in "source tiering" "evidence card" "blocking" "output template"; do
    grep -qi "$section" ~/.openclaw/workspace/skills/deep-research/SKILL.md \
      && echo "✓ $section" \
      || echo "✗ MISSING: $section"
done
```

**Step 4: Confirm to user**

Report: installed path, version, line count, and trigger phrases.

---

## Post-Installation

The skill activates when the user says:
- "帮我研究一下..." / "研究一下..."
- "你去查一查..." / "搜索..."
- "核实..." / "确认一下..."
- "调查..."
- Or any multi-source research request

## Uninstall

```bash
clawhub uninstall ashanzzz-deep-research
# Or manually:
rm -rf ~/.openclaw/workspace/skills/deep-research
```
