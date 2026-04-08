# openclaw-person-skills

> Ashan's personal OpenClaw skills — published to ClawHub for one-command installation.

---

## Quick Install

### One Command (All Skills)

```bash
clawhub install ashanzzz-vikunja-task-api
clawhub install ashanzzz-deep-research
clawhub install ashanzzz-skill-vetter
```

### Or Install All at Once

```bash
for SKILL in vikunja-task-api deep-research skill-vetter proactivity self-improving books-growth-advisor erpnext-invoice-detail-export erpnext-monthly-invoice-export erpnext-account-report business-analysis; do
    clawhub install ashanzzz-$SKILL 2>/dev/null || echo "⚠ $SKILL not yet on ClawHub"
done
```

### Individual Skills

| Skill | ClawHub Install | Description |
|-------|----------------|-------------|
| `vikunja-task-api` | `clawhub install ashanzzz-vikunja-task-api` | Full Vikunja v2 API integration |
| `deep-research` | `clawhub install ashanzzz-deep-research` | 8-step research methodology |
| `skill-vetter` | `clawhub install ashanzzz-skill-vetter` | Security vetting before installing skills |
| `erpnext-invoice-detail-export` | `clawhub install erpnext-invoice-detail-export` | ERPNext 发票明细导出：按发票号导出含规格型号/备注的明细 |
| `erpnext-monthly-invoice-export` | `clawhub install erpnext-monthly-invoice-export` | ERPNext 月度发票导出：按公司+月份导出采购发票 |
| `erpnext-account-report` | *(自建技能)* | ERPNext 账单导出：GL→PE→PI→物料自动勾稽，每行一个物料明细 |
| `business-analysis` | *(自建技能)* | 商业分析：四轮验证+十二维分析+数据源URL |
| `books-growth-advisor` | *(自建技能)* | 基于9本管理书回答职业发展/工厂/管理/人际问题 |
| `proactivity` | *(自建技能)* | 主动工作流：预判需求、主动巡检 |
| `self-improving` | *(自建技能)* | 自学习：捕获错误与纠正 |
| `skill-creator` | *(自建技能)* | Skill 创建/编辑/审核完整指南 |
| `purchase-invoice-classifier` | *(自建技能)* | 采购发票分类 |
| `purchase-wire-transfer-reconcile` | *(自建技能)* | 采购电汇对账 |
| `finance-reconcile-workbook` | *(自建技能)* | 财务对账工作簿 |
| `finance-remark-mapping` | *(自建技能)* | 财务备注映射 |
| `book-learner` | *(自建技能)* | 图书切片阅读与笔记生成 |
| `book-audit` | *(自建技能)* | 图书笔记完整性复核 |
| `news-tracker` | *(自建技能)* | 新闻跟踪 |

Browse all on ClawHub: https://clawhub.ai/ashanzzz

---

## Manual / Offline Installation

If `clawhub install` is unavailable, use curl:

```bash
# Example: erpnext-account-report
SKILL_NAME=erpnext-account-report
mkdir -p ~/.openclaw/workspace/skills/$SKILL_NAME
curl -fsSL https://raw.githubusercontent.com/ashanzzz/openclaw-person-skills/main/skills/$SKILL_NAME/SKILL.md \
  -o ~/.openclaw/workspace/skills/$SKILL_NAME/SKILL.md
```

---

## Repository Scope

**Contains:** Skill本体 (`SKILL.md`), scripts, references, installation guides
**Does NOT contain:** Runtime data, ebook content, caches
