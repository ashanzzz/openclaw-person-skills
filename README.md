# openclaw-person-skills

> Ashan's personal OpenClaw skills collection — published to ClawHub for easy installation.

## Quick Install (Pick One)

### Human: Let an AI Agent Do It

```
Install and configure the openclaw-person-skills collection by following:
https://raw.githubusercontent.com/ashanzzz/openclaw-person-skills/main/README.md
```

Then ask your AI agent: "Show me available skills and install [skill name]"

### Human: Manual One-Liner

```bash
# Install any skill by name
curl -fsSL https://raw.githubusercontent.com/ashanzzz/openclaw-person-skills/main/skills/[SKILL-NAME]/INSTALL.md | bash
```

### AI Agent: Install All Skills

```bash
# For each skill, curl its INSTALL.md and follow steps
SKILLS="vikunja-task-api deep-research skill-vetter unraidclaw proactivity self-improving books-growth-advisor erpnext-monthly-invoice-export"

for SKILL in $SKILLS; do
    echo "=== Installing: $SKILL ==="
    curl -fsSL https://raw.githubusercontent.com/ashanzzz/openclaw-person-skills/main/skills/$SKILL/INSTALL.md \
      && echo "=== Done: $SKILL ==="
done
```

### AI Agent: Install Single Skill

```bash
curl -fsSL https://raw.githubusercontent.com/ashanzzz/openclaw-person-skills/main/skills/[SKILL-NAME]/INSTALL.md
# Then follow the Step-by-step instructions in the file
```

---

## Repository Scope

**This repo contains:**
- Skill本体 (`skills/<name>/SKILL.md`)
- Skill dependencies (scripts, references, assets)
- Skill installation guides (`skills/<name>/INSTALL.md`)

**This repo does NOT contain:**
- Runtime data or working files
- Original ebook content
- Temporary caches or slices

---

## Available Skills

| Skill | Description | Install File |
|-------|-------------|-------------|
| `vikunja-task-api` | Full Vikunja v2 API integration | [INSTALL.md](./skills/vikunja-task-api/INSTALL.md) |
| `deep-research` | 8-step research methodology + 4-tier source credibility | [INSTALL.md](./skills/deep-research/INSTALL.md) |
| `skill-vetter` | Security-first skill vetting before installing any skill | [INSTALL.md](./skills/skill-vetter/INSTALL.md) |
| `unraidclaw` | Unraid server management via UnraidCLaW REST API | [INSTALL.md](./skills/unraidclaw/INSTALL.md) |
| `proactivity` | Proactive agent behavior framework | [INSTALL.md](./skills/proactivity/INSTALL.md) |
| `self-improving` | Self-reflection + self-criticism + self-learning | [INSTALL.md](./skills/self-improving/INSTALL.md) |
| `books-growth-advisor` | Management classics advisor (9 books) | [INSTALL.md](./skills/books-growth-advisor/INSTALL.md) |
| `erpnext-monthly-invoice-export` | ERPNext monthly invoice export | [INSTALL.md](./skills/erpnext-monthly-invoice-export/INSTALL.md) |
| `erpnext-invoice-detail-export` | ERPNext invoice detail export | [INSTALL.md](./skills/erpnext-invoice-detail-export/INSTALL.md) |
| `finance-reconcile-workbook` | Financial reconciliation workbook generator | [INSTALL.md](./skills/finance-reconcile-workbook/INSTALL.md) |
| `purchase-wire-transfer-reconcile` | Wire transfer reconciliation | [INSTALL.md](./skills/purchase-wire-transfer-reconcile/INSTALL.md) |
| `news-tracker` | News tracking and archiving | [INSTALL.md](./skills/news-tracker/INSTALL.md) |
| `book-learner` | Book reading and note generation | [INSTALL.md](./skills/book-learner/INSTALL.md) |
| `book-audit` | Book note integrity audit | [INSTALL.md](./skills/book-audit/INSTALL.md) |

---

## ClawHub Publication

All skills are published to ClawHub under the author `ashanzzz`:

```bash
# Install from ClawHub (if your OpenClaw has clawhub CLI)
clawhub install ashanzzz-vikunja-task-api
clawhub install ashanzzz-deep-research
# ... more skills coming
```

Browse all: https://clawhub.ai/ashanzzz

---

## For AI Agents: Detecting Installed Skills

```bash
INSTALLED_SKILLS=""
for DIR in ~/.openclaw/workspace/skills/*/; do
    if [ -f "$DIR/SKILL.md" ]; then
        NAME=$(basename "$DIR")
        VER=$(grep "^version:" "$DIR/SKILL.md" 2>/dev/null | cut -d: -f2 | tr -d ' ' || echo "unknown")
        INSTALLED_SKILLS="$INSTALLED_SKILLS\n  ✓ $NAME (v$VER)"
    fi
done
echo "Installed skills:$INSTALLED_SKILLS"
```
