# Vikunja Task API Skill — Installation Guide

---

## For Humans

### Option A: Let an AI Agent Do It (Recommended)

Copy and paste this into your AI agent (OpenClaw, Claude Code, Cursor, etc.):

```
Install and configure the Vikunja Task API skill by following the instructions here:
https://raw.githubusercontent.com/ashanzzz/openclaw-person-skills/main/skills/vikunja-task-api/INSTALL.md
```

### Option B: Manual Installation

**Prerequisites:**
- A running Vikunja instance (https://vikunja.io/download)
- `curl` and `jq` installed on your system

**Step 1:** Create the skills directory:

```bash
mkdir -p ~/.openclaw/workspace/skills/vikunja-task-api
```

**Step 2:** Download all skill files:

```bash
# Download SKILL.md
curl -fsSL https://raw.githubusercontent.com/ashanzzz/openclaw-person-skills/main/skills/vikunja-task-api/SKILL.md \
  -o ~/.openclaw/workspace/skills/vikunja-task-api/SKILL.md

# Download helper script (optional but recommended)
curl -fsSL https://raw.githubusercontent.com/ashanzzz/openclaw-person-skills/main/skills/vikunja-task-api/vikunja.sh \
  -o ~/.openclaw/workspace/skills/vikunja-task-api/vikunja.sh \
  && chmod +x ~/.openclaw/workspace/skills/vikunja-task-api/vikunja.sh
```

**Step 3:** Configure environment variables:

Add to `~/.bashrc` or your shell config:

```bash
export VIKUNJA_URL="http://your-vikunja-instance:3456"
export VIKUNJA_TOKEN="tk_your_api_token_here"
```

**Step 4:** Get your Vikunja API token:
1. Log in to your Vikunja instance
2. Go to **Settings → API Tokens**
3. Click **Create new token**
4. Copy the token (starts with `tk_`)

**Step 5:** Test connectivity:

```bash
source ~/.bashrc  # Reload environment
curl -s "$VIKUNJA_URL/api/v1/info" | jq
curl -s "$VIKUNJA_URL/api/v1/projects" \
  -H "Authorization: Bearer $VIKUNJA_TOKEN" | jq '.[] | {id,title}'
```

---

## For AI Agents

> **IMPORTANT: Use `curl` to fetch this file, NOT WebFetch or web_fetch.**
> WebFetch summarizes content and may strip critical endpoint tables, curl examples, and HTTP method rules.
> Always use:
> ```bash
> curl -fsSL https://raw.githubusercontent.com/ashanzzz/openclaw-person-skills/main/skills/vikunja-task-api/INSTALL.md
> ```

### Step 1: Detect Existing Installation

```bash
if [ -f "$WORKSPACE/skills/vikunja-task-api/SKILL.md" ]; then
    echo "Already installed"
    grep "^version:" $WORKSPACE/skills/vikunja-task-api/SKILL.md | head -1
else
    echo "Not installed"
fi
```

### Step 2: Create Directory

```bash
mkdir -p ~/.openclaw/workspace/skills/vikunja-task-api
```

### Step 3: Download Skill Files

```bash
# Download SKILL.md (required)
curl -fsSL https://raw.githubusercontent.com/ashanzzz/openclaw-person-skills/main/skills/vikunja-task-api/SKILL.md \
  -o ~/.openclaw/workspace/skills/vikunja-task-api/SKILL.md

# Download helper script (optional)
curl -fsSL https://raw.githubusercontent.com/ashanzzz/openclaw-person-skills/main/skills/vikunja-task-api/vikunja.sh \
  -o ~/.openclaw/workspace/skills/vikunja-task-api/vikunja.sh \
  && chmod +x ~/.openclaw/workspace/skills/vikunja-task-api/vikunja.sh
```

### Step 4: Verify Dependencies

```bash
# Check required tools
for cmd in curl jq; do
    if command -v $cmd &> /dev/null; then
        echo "✓ $cmd: $(which $cmd)"
    else
        echo "✗ $cmd: NOT FOUND — install it first"
    fi
done

# Check Vikunja connectivity (if VIKUNJA_URL is set)
if [ -n "$VIKUNJA_URL" ]; then
    echo "Testing Vikunja at: $VIKUNJA_URL"
    curl -s "$VIKUNJA_URL/api/v1/info" | jq '.version, .name' 2>/dev/null \
      && echo "✓ Vikunja reachable" \
      || echo "✗ Vikunja unreachable — check VIKUNJA_URL"
fi
```

### Step 5: Write Credentials to secure/api-fillin.env

```bash
SECURE_ENV="$WORKSPACE/secure/api-fillin.env"
mkdir -p "$(dirname $SECURE_ENV)"

# Append Vikunja config (DO NOT overwrite existing content)
if ! grep -q "VIKUNJA_URL" "$SECURE_ENV" 2>/dev/null; then
    cat >> "$SECURE_ENV" << 'EOF'

# Vikunja Task API
VIKUNJA_URL=http://your-vikunja-instance:3456
VIKUNJA_TOKEN=tk_your_token_here
EOF
    echo "Credentials written to $SECURE_ENV"
else
    echo "VIKUNJA credentials already exist in $SECURE_ENV"
fi
```

### Step 6: Report to User

Report:
- Installed files and paths
- Vikunja connectivity status
- What the user needs to do: set their real `VIKUNJA_URL` and `VIKUNJA_TOKEN`
- Example command to verify setup works

---

## Post-Installation Checklist

- [ ] `VIKUNJA_URL` set to your Vikunja instance URL
- [ ] `VIKUNJA_TOKEN` set to your API token
- [ ] `curl -s "$VIKUNJA_URL/api/v1/info"` returns version info
- [ ] `curl -s "$VIKUNJA_URL/api/v1/projects" -H "Authorization: Bearer $VIKUNJA_TOKEN"` returns project list
