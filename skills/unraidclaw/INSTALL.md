# UnraidCLaW Skill — Installation

---

## For Humans

### Option A: One Command Install (Recommended)

```bash
clawhub install ashanzzz-unraidclaw
```

### Option B: Manual Install

```bash
mkdir -p ~/.openclaw/workspace/skills/unraidclaw

# Download SKILL.md
curl -fsSL https://raw.githubusercontent.com/ashanzzz/openclaw-person-skills/main/skills/unraidclaw/SKILL.md \
  -o ~/.openclaw/workspace/skills/unraidclaw/SKILL.md

# Download helper scripts
curl -fsSL https://raw.githubusercontent.com/ashanzzz/openclaw-person-skills/main/skills/unraidclaw/scripts/opencode_install.sh \
  -o ~/.openclaw/workspace/skills/unraidclaw/scripts/opencode_install.sh
curl -fsSL https://raw.githubusercontent.com/ashanzzz/openclaw-person-skills/main/skills/unraidclaw/scripts/unraid_common.sh \
  -o ~/.openclaw/workspace/skills/unraidclaw/scripts/unraid_common.sh
curl -fsSL https://raw.githubusercontent.com/ashanzzz/openclaw-person-skills/main/skills/unraidclaw/scripts/unraid_docker.sh \
  -o ~/.openclaw/workspace/skills/unraidclaw/scripts/unraid_docker.sh
chmod +x ~/.openclaw/workspace/skills/unraidclaw/scripts/*.sh
```

### Required Setup After Install

**Prerequisites:**
- Unraid server with UnraidCLaW plugin installed (https://github.com/emaspa/unraidclaw)
- Get your UnraidCLaW API key from: **Settings → UnraidCLaW → API Key**

**Add to your environment:**

```bash
# Add to ~/.bashrc or shell config
export UNRAID_HOST="http://your-unraid-ip:9876"
export UNRAIDCLAW_TOKEN="your_unraidclaw_api_key_here"
```

---

## For AI Agents

### Primary Method: Use `clawhub install`

```bash
clawhub install ashanzzz-unraidclaw
```

### Step-by-Step (if clawhub install is unavailable)

> **IMPORTANT: If `clawhub install` is unavailable, use `curl` as fallback.**
> NEVER use WebFetch.

**Step 1: Check if already installed**

```bash
if [ -f "$WORKSPACE/skills/unraidclaw/SKILL.md" ]; then
    echo "Already installed"
    grep "^description:" $WORKSPACE/skills/unraidclaw/SKILL.md | head -1 | cut -c1-80
else
    echo "Not installed"
fi
```

**Step 2: Download files**

```bash
mkdir -p ~/.openclaw/workspace/skills/unraidclaw/scripts

curl -fsSL https://raw.githubusercontent.com/ashanzzz/openclaw-person-skills/main/skills/unraidclaw/SKILL.md \
  -o ~/.openclaw/workspace/skills/unraidclaw/SKILL.md

for script in opencode_install.sh unraid_common.sh unraid_docker.sh; do
    curl -fsSL https://raw.githubusercontent.com/ashanzzz/openclaw-person-skills/main/skills/unraidclaw/scripts/$script \
      -o ~/.openclaw/workspace/skills/unraidclaw/scripts/$script
done
chmod +x ~/.openclaw/workspace/skills/unraidclaw/scripts/*.sh
```

**Step 3: Verify UnraidCLaW connectivity**

```bash
curl -s -k "$UNRAID_HOST/api/health" \
  -H "x-api-key: $UNRAIDCLAW_TOKEN" | jq '.version, .status' \
  && echo "✓ UnraidCLaW reachable" \
  || echo "✗ Cannot reach UnraidCLaW"
```

**Step 4: Prompt user for credentials if missing**

If `UNRAID_HOST` or `UNRAIDCLAW_TOKEN` is not set, ask the user for:
- Their Unraid IP address (e.g. `http://192.168.1.100:9876`)
- Their UnraidCLaW API key

**Step 5: Write credentials to secure storage**

```bash
SECURE_ENV="$WORKSPACE/secure/api-fillin.env"
mkdir -p "$(dirname $SECURE_ENV)"
if ! grep -q "UNRAIDCLAW_TOKEN" "$SECURE_ENV" 2>/dev/null; then
    cat >> "$SECURE_ENV" << 'EOF'

# UnraidCLaW API
UNRAID_HOST=http://your-unraid-ip:9876
UNRAIDCLAW_TOKEN=your_token_here
EOF
fi
```

**Step 6: Report to user**

Report: installed files, UnraidCLaW version (from `/api/health`), and what the user needs to configure.

---

## Post-Installation Checklist

- [ ] UnraidCLaW plugin installed on Unraid server
- [ ] `UNRAID_HOST` set to your Unraid IP:port
- [ ] `UNRAIDCLAW_TOKEN` set to your API key
- [ ] `curl -k "$UNRAID_HOST/api/health"` returns JSON with version
- [ ] UnraidCLaW version is v0.1.27 or newer

## Uninstall

```bash
clawhub uninstall ashanzzz-unraidclaw
# Or manually:
rm -rf ~/.openclaw/workspace/skills/unraidclaw
```
