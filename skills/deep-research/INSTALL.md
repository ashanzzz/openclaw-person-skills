# Deep Research Skill — Installation Guide

---

## For Humans

### Option A: Let an AI Agent Do It (Recommended)

Copy and paste this into your AI agent (OpenClaw, Claude Code, Cursor, etc.):

```
Install and configure the Deep Research skill by following the instructions here:
https://raw.githubusercontent.com/ashanzzz/openclaw-person-skills/main/skills/deep-research/INSTALL.md
```

### Option B: Manual Installation

**Step 1:** Create the skills directory if it doesn't exist:

```bash
mkdir -p ~/.openclaw/workspace/skills/deep-research
```

**Step 2:** Download the SKILL.md file:

```bash
curl -fsSL https://raw.githubusercontent.com/ashanzzz/openclaw-person-skills/main/skills/deep-research/SKILL.md \
  -o ~/.openclaw/workspace/skills/deep-research/SKILL.md
```

**Step 3:** Verify the file was downloaded correctly:

```bash
head -20 ~/.openclaw/workspace/skills/deep-research/SKILL.md
```

---

## For AI Agents

> **IMPORTANT: Use `curl` to fetch this file, NOT WebFetch or web_fetch.**
> WebFetch summarizes content and may strip critical formatting, step sequences, and blocking rules.
> Always use:
> ```bash
> curl -fsSL https://raw.githubusercontent.com/ashanzzz/openclaw-person-skills/main/skills/deep-research/INSTALL.md
> ```

### Step 1: Detect Existing Installation

Check if the skill is already installed:

```bash
if [ -f "$WORKSPACE/skills/deep-research/SKILL.md" ]; then
    echo "Already installed at: $WORKSPACE/skills/deep-research/SKILL.md"
    echo "Version: $(grep '^version:' $WORKSPACE/skills/deep-research/SKILL.md | head -1)"
else
    echo "Not installed"
fi
```

Where `$WORKSPACE` is typically `~/.openclaw/workspace`.

### Step 2: Create Directory

```bash
mkdir -p ~/.openclaw/workspace/skills/deep-research
```

### Step 3: Download SKILL.md

```bash
curl -fsSL https://raw.githubusercontent.com/ashanzzz/openclaw-person-skills/main/skills/deep-research/SKILL.md \
  -o ~/.openclaw/workspace/skills/deep-research/SKILL.md

if [ $? -eq 0 ]; then
    echo "Downloaded successfully"
    wc -l ~/.openclaw/workspace/skills/deep-research/SKILL.md
else
    echo "Download failed"
fi
```

### Step 4: Verify Content Integrity

```bash
# Check critical sections exist
for section in "trigger" "source tiering" "evidence card" "blocking" "output template"; do
    if grep -qi "$section" ~/.openclaw/workspace/skills/deep-research/SKILL.md; then
        echo "✓ Found: $section"
    else
        echo "✗ MISSING: $section"
    fi
done
```

### Step 5: Confirm to User

Report completion with:
- Installed path
- Skill version (from `version:` frontmatter field)
- Total line count
- Which trigger phrases this skill activates on

---

## Post-Installation

After installing, the skill activates when the user says:
- "帮我研究一下..." / "研究一下..."
- "你去查一查..." / "搜索..."
- "核实..." / "确认一下..."
- "调查..."

The skill enforces: 8-step research process, 4-tier source credibility, multi-source cross-verification, and blocking rules before output.
