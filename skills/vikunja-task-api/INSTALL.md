# Vikunja Task API Skill — Installation

---

## For Humans

### Option A: One Command Install (Recommended)

```bash
clawhub install ashanzzz-vikunja-task-api
```

### Option B: Manual Install

```bash
mkdir -p ~/.openclaw/workspace/skills/vikunja-task-api

# Download SKILL.md
curl -fsSL https://raw.githubusercontent.com/ashanzzz/openclaw-person-skills/main/skills/vikunja-task-api/SKILL.md \
  -o ~/.openclaw/workspace/skills/vikunja-task-api/SKILL.md

# Download helper script (optional)
curl -fsSL https://raw.githubusercontent.com/ashanzzz/openclaw-person-skills/main/skills/vikunja-task-api/vikunja.sh \
  -o ~/.openclaw/workspace/skills/vikunja-task-api/vikunja.sh \
  && chmod +x ~/.openclaw/workspace/skills/vikunja-task-api/vikunja.sh
```

### Required Setup After Install

**Get your Vikunja API token:**
1. Log in to your Vikunja instance
2. Go to **Settings → API Tokens**
3. Click **Create new token** → copy it (starts with `tk_`)

**Add to your environment:**

```bash
# Add to ~/.bashrc or shell config
export VIKUNJA_URL="http://your-vikunja-instance:3456"
export VIKUNJA_TOKEN="tk_your_token_here"
```

---

## For AI Agents

### Primary Method: Use `clawhub install`

```bash
clawhub install ashanzzz-vikunja-task-api
```

### Step-by-Step (if clawhub install is unavailable)

> **IMPORTANT: If `clawhub install` is unavailable, use `curl` as fallback.**
> NEVER use WebFetch.

**Step 1: Check if already installed**

```bash
if [ -f "$WORKSPACE/skills/vikunja-task-api/SKILL.md" ]; then
    echo "Already installed"
    grep "^version:" $WORKSPACE/skills/vikunja-task-api/SKILL.md | head -1
else
    echo "Not installed"
fi
```

**Step 2: Download files**

```bash
mkdir -p ~/.openclaw/workspace/skills/vikunja-task-api

curl -fsSL https://raw.githubusercontent.com/ashanzzz/openclaw-person-skills/main/skills/vikunja-task-api/SKILL.md \
  -o ~/.openclaw/workspace/skills/vikunja-task-api/SKILL.md

curl -fsSL https://raw.githubusercontent.com/ashanzzz/openclaw-person-skills/main/skills/vikunja-task-api/vikunja.sh \
  -o ~/.openclaw/workspace/skills/vikunja-task-api/vikunja.sh \
  && chmod +x ~/.openclaw/workspace/skills/vikunja-task-api/vikunja.sh
```

**Step 3: Verify Vikunja connectivity**

```bash
curl -s "$VIKUNJA_URL/api/v1/info" | jq '.version, .name' \
  && echo "✓ Vikunja reachable" \
  || echo "✗ Vikunja unreachable"
```

**Step 4: Prompt user for credentials if missing**

If `VIKUNJA_URL` or `VIKUNJA_TOKEN` is not set, ask the user for:
- Their Vikunja instance URL
- Their API token (from Settings → API Tokens)

**Step 5: Write credentials to secure storage**

```bash
SECURE_ENV="$WORKSPACE/secure/api-fillin.env"
mkdir -p "$(dirname $SECURE_ENV)"
if ! grep -q "VIKUNJA_URL" "$SECURE_ENV" 2>/dev/null; then
    cat >> "$SECURE_ENV" << 'EOF'

# Vikunja Task API
VIKUNJA_URL=http://your-vikunja-instance:3456
VIKUNJA_TOKEN=tk_your_token_here
EOF
fi
```

**Step 6: Report to user**

Report: installed files, connectivity status, and what the user needs to configure.

---

## Post-Installation Checklist

- [ ] `clawhub install ashanzzz-vikunja-task-api` ran successfully
- [ ] `VIKUNJA_URL` set to your Vikunja instance
- [ ] `VIKUNJA_TOKEN` set to your API token
- [ ] `curl -s "$VIKUNJA_URL/api/v1/info"` returns version info
- [ ] `curl -s "$VIKUNJA_URL/api/v1/projects" -H "Authorization: Bearer $VIKUNJA_TOKEN"` returns projects

## Uninstall

```bash
clawhub uninstall ashanzzz-vikunja-task-api
# Or manually:
rm -rf ~/.openclaw/workspace/skills/vikunja-task-api
```
