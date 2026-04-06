# openclaw-person-skills

> Ashan's personal OpenClaw skills — published to ClawHub for one-command installation.

---

## Quick Install

### One Command (All Skills)

```bash
clawhub install ashanzzz-vikunja-task-api
clawhub install ashanzzz-deep-research
clawhub install ashanzzz-skill-vetter
clawhub install ashanzzz-unraidclaw
```

### Or Install All at Once

```bash
for SKILL in vikunja-task-api deep-research skill-vetter unraidclaw proactivity self-improving books-growth-advisor; do
    clawhub install ashanzzz-$SKILL 2>/dev/null || echo "⚠ $SKILL not yet on ClawHub"
done
```

---

## Available Skills

| Skill | ClawHub Install | Description |
|-------|----------------|-------------|
| `vikunja-task-api` | `clawhub install ashanzzz-vikunja-task-api` | Full Vikunja v2 API integration |
| `deep-research` | `clawhub install ashanzzz-deep-research` | 8-step research methodology |
| `skill-vetter` | `clawhub install ashanzzz-skill-vetter` | Security vetting before installing skills |
| `unraidclaw` | `clawhub install ashanzzz-unraidclaw` | Unraid server management |
| `proactivity` | *(pending ClawHub publish)* | Proactive agent behavior |
| `self-improving` | *(pending ClawHub publish)* | Self-reflection + learning |
| `books-growth-advisor` | *(pending ClawHub publish)* | Management classics advisor |
| `erpnext-*` | *(pending ClawHub publish)* | ERPNext integrations |
| `finance-*` | *(pending ClawHub publish)* | Financial reconciliation |
| `news-tracker` | *(pending ClawHub publish)* | News tracking |
| `book-*` | *(pending ClawHub publish)* | Book knowledge pipeline |

Browse all on ClawHub: https://clawhub.ai/ashanzzz

---

## Manual / Offline Installation

If `clawhub install` is unavailable, use curl:

```bash
SKILL_NAME=vikunja-task-api
mkdir -p ~/.openclaw/workspace/skills/$SKILL_NAME
curl -fsSL https://raw.githubusercontent.com/ashanzzz/openclaw-person-skills/main/skills/$SKILL_NAME/SKILL.md \
  -o ~/.openclaw/workspace/skills/$SKILL_NAME/SKILL.md
```

> **IMPORTANT:** Use `curl`, NOT WebFetch. WebFetch strips formatting and critical details.

---

## For AI Agents: Install Single Skill

```bash
# Primary: use clawhub
clawhub install ashanzzz-[skill-name]

# Fallback: curl
curl -fsSL https://raw.githubusercontent.com/ashanzzz/openclaw-person-skills/main/skills/[skill-name]/INSTALL.md
# Then follow the step-by-step instructions in the file
```

---

## For AI Agents: Detect Installed Skills

```bash
for DIR in ~/.openclaw/workspace/skills/*/; do
    if [ -f "$DIR/SKILL.md" ]; then
        NAME=$(basename "$DIR")
        VER=$(grep "^version:" "$DIR/SKILL.md" 2>/dev/null | cut -d: -f2 | tr -d ' ' || echo "unknown")
        echo "  ✓ $NAME (v$VER)"
    fi
done
```

---

## Repository Scope

**Contains:** Skill本体 (`SKILL.md`), scripts, references, installation guides (`INSTALL.md`)
**Does NOT contain:** Runtime data, ebook content, caches
