# UnraidCLaW Skill — Installation Guide

---

## For Humans

### Option A: Let an AI Agent Do It (Recommended)

Copy and paste this into your AI agent (OpenClaw, Claude Code, Cursor, etc.):

```
Install and configure the UnraidCLaW skill by following the instructions here:
https://raw.githubusercontent.com/ashanzzz/openclaw-person-skills/main/skills/unraidclaw/INSTALL.md
```

### Option B: Manual Installation

**Prerequisites:**
- Unraid server with UnraidCLaW plugin installed (https://github.com/emaspa/unraidclaw)
- `curl` installed (standard on most systems)

**Step 1:** Verify UnraidCLaW is installed on your Unraid server:

Log into your Unraid web UI → **Settings → UnraidCLaW**
If not installed, follow instructions at: https://github.com/emaspa/unraidclaw

**Step 2:** Get your UnraidCLaW API key:

1. Go to **Settings → UnraidCLaW → API Key**
2. Copy the API key (starts with `unraidclaw_...`)

**Step 3:** Get your Unraid IP address:

Your Unraid web UI URL, e.g. `http://192.168.1.100`

**Step 4:** Create the skills directory:

```bash
mkdir -p ~/.openclaw/workspace/skills/unraidclaw
```

**Step 5:** Download the SKILL.md:

```bash
curl -fsSL https://raw.githubusercontent.com/ashanzzz/openclaw-person-skills/main/skills/unraidclaw/SKILL.md \
  -o ~/.openclaw/workspace/skills/unraidclaw/SKILL.md
```

**Step 6:** Write credentials to secure storage:

```bash
cat >> ~/.openclaw/workspace/secure/api-fillin.env << 'EOF'

# UnraidCLaW API
UNRAID_HOST=http://your-unraid-ip:9876
UNRAIDCLAW_TOKEN=your_unraidclaw_api_key_here
EOF
```

Replace `your-unraid-ip` and `your_unraidclaw_api_key_here` with your actual values.

**Step 7:** Test connectivity:

```bash
curl -s -k "$UNRAID_HOST/api/health" \
  -H "x-api-key: $UNRAIDCLAW_TOKEN" | jq
```

---

## For AI Agents

> **IMPORTANT: Use `curl` to fetch this file, NOT WebFetch or web_fetch.**
> Always use:
> ```bash
> curl -fsSL https://raw.githubusercontent.com/ashanzzz/openclaw-person-skills/main/skills/unraidclaw/INSTALL.md
> ```

### Step 1: Detect Existing Installation

```bash
if [ -f "$WORKSPACE/skills/unraidclaw/SKILL.md" ]; then
    echo "Already installed"
    grep "^description:" $WORKSPACE/skills/unraidclaw/SKILL.md | head -1
else
    echo "Not installed"
fi
```

### Step 2: Create Directory

```bash
mkdir -p ~/.openclaw/workspace/skills/unraidclaw
```

### Step 3: Download SKILL.md

```bash
curl -fsSL https://raw.githubusercontent.com/ashanzzz/openclaw-person-skills/main/skills/unraidclaw/SKILL.md \
  -o ~/.openclaw/workspace/skills/unraidclaw/SKILL.md
```

### Step 4: Verify Health Endpoint (Test UnraidCLaW Connectivity)

```bash
# Try to reach UnraidCLaW health endpoint
curl -s -k https://YOUR_UNRAID_IP:9876/api/health \
  -H "x-api-key: YOUR_UNRAIDCLAW_TOKEN" 2>/dev/null | jq '.version, .status' \
  && echo "✓ UnraidCLaW reachable" \
  || echo "✗ Cannot reach UnraidCLaW — check host URL and API key"
```

### Step 5: Prompt User for Credentials if Missing

```bash
# Check if credentials are already set in secure/api-fillin.env
if grep -q "UNRAIDCLAW_TOKEN" $WORKSPACE/secure/api-fillin.env 2>/dev/null; then
    echo "✓ UnraidCLaW credentials found"
else
    echo "⚠ UNRAIDCLAW_TOKEN not found in secure/api-fillin.env"
    echo "Please provide:"
    echo "  1. Unraid IP address (e.g. http://192.168.1.100:9876)"
    echo "  2. UnraidCLaW API key (from Unraid Settings → UnraidCLaW → API Key)"
fi
```

### Step 6: Write Credentials if Provided

```bash
# Only write if user provided values (replace placeholder values)
SECURE_ENV="$WORKSPACE/secure/api-fillin.env"
if [ -n "$UNRAID_HOST" ] && [ -n "$UNRAIDCLAW_TOKEN" ]; then
    mkdir -p "$(dirname $SECURE_ENV)"
    if ! grep -q "UNRAIDCLAW_TOKEN" "$SECURE_ENV" 2>/dev/null; then
        cat >> "$SECURE_ENV" << 'EOF'

# UnraidCLaW API
UNRAID_HOST=http://your-unraid-ip:9876
UNRAIDCLAW_TOKEN=your_token_here
EOF
    fi
fi
```

### Step 7: Report to User

Report:
- Installation status
- UnraidCLaW version if reachable (from `/api/health`)
- What the user needs to provide if credentials are missing

---

## Post-Installation Checklist

- [ ] UnraidCLaW plugin installed on Unraid server
- [ ] `UNRAID_HOST` set to your Unraid IP:port
- [ ] `UNRAIDCLAW_TOKEN` set to your API key
- [ ] `curl -k "$UNRAID_HOST/api/health"` returns JSON with version
- [ ] UnraidCLaW version is v0.1.27 or newer (check for updates)
