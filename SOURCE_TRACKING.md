# Skill Source Tracking

> 记录每个技能的来源，方便维护和分发决策。
> 更新时间：2026-04-06

---

## 判断规则

| 来源 | 说明 |
|------|------|
| **自建** | 我们自己写的 skill |
| **外部下载** | 从 ClawHub/GitHub/其他用户处安装的原始 skill |
| **Fork 自建** | 外部下载后我们做了大量修改/本地化的 skill |

---

## 同步方式说明

| 同步目标 | 内容 | 同步方式 |
|---------|------|---------|
| **本地 workspace** | 所有技能的工作副本 | 实时读写，`~/.openclaw/workspace/skills/` |
| **GitHub 公共仓库** | 公开分享的技能 | `git push` 到 `ashanzzz/openclaw-person-skills` |
| **ClawHub** | 公共技能市场 | `clawhub publish` 发布/更新 |
| **GitHub 私人仓库** | 私人资产备份 | `git push` 到 `ashanzzz/private-life` |

---

## 技能清单

### 一、我们自建并上传到 ClawHub

| Skill | ClawHub Slug | 版本 | 地址 |
|-------|-------------|------|------|
| `deep-research` | `ashanzzz-deep-research` | 1.2.0 | https://clawhub.ai/ashanzzz/ashanzzz-deep-research |
| `vikunja-task-api` | `ashanzzz-vikunja-task-api` | 2.4.0 | https://clawhub.ai/ashanzzz/ashanzzz-vikunja-task-api |
| `skill-vetter` | `ashanzzz-skill-vetter` | 1.2.0 | https://clawhub.ai/ashanzzz/ashanzzz-skill-vetter |
| `unraidclaw` | `ashanzzz-unraidclaw` | 1.2.0 | https://clawhub.ai/ashanzzz/ashanzzz-unraidclaw |
| `sure-api` | `sure-api` | 1.0.0 | https://clawhub.ai/ashanzzz/sure-api |

---

### 二、我们自建，仅在 GitHub 仓库（内部管理，不上传）

| Skill | 说明 | GitHub 路径 |
|-------|------|------------|
| `books-growth-advisor` | 基于9本管理书的顾问框架 | `openclaw-person-skills/skills/books-growth-advisor/` |
| `erpnext-monthly-invoice-export` | ERPNext 月度发票导出 | `openclaw-person-skills/skills/erpnext-monthly-invoice-export/` |
| `erpnext-invoice-detail-export` | ERPNext 发票明细导出 | `openclaw-person-skills/skills/erpnext-invoice-detail-export/` |
| `finance-reconcile-workbook` | 财务对账工作簿生成器 | `openclaw-person-skills/skills/finance-reconcile-workbook/` |
| `finance-remark-mapping` | 财务备注映射 | `openclaw-person-skills/skills/finance-remark-mapping/` |
| `purchase-wire-transfer-reconcile` | 采购电汇对账 | `openclaw-person-skills/skills/purchase-wire-transfer-reconcile/` |
| `purchase-invoice-classifier` | 采购发票分类 | `openclaw-person-skills/skills/purchase-invoice-classifier/` |
| `reconcile-output-format` | 对账输出格式化 | `openclaw-person-skills/skills/reconcile-output-format/` |
| `book-learner` | 图书切片阅读与笔记生成 | `openclaw-person-skills/skills/book-learner/` |
| `book-audit` | 图书笔记完整性审计 | `openclaw-person-skills/skills/book-audit/` |
| `book-notes-sop` | 大任务一次性执行 SOP | `openclaw-person-skills/skills/book-notes-sop/` |
| `repo-structure-manager` | 仓库结构治理 | `openclaw-person-skills/skills/repo-structure-manager/` |
| `news-tracker` | 新闻追踪存档 | `openclaw-person-skills/skills/news-tracker/` |

---

### 三、我们自建，仅本地（内部管理）

| Skill | 说明 | 存放位置 |
|-------|------|---------|
| `ruijie-noc-donglihu-watch` | 锐捷 NOC 监控脚本 | `~/.openclaw/workspace/skills/ruijie-noc-donglihu-watch/` |

---

### 四、外部下载，安装在本地（内部管理）

| Skill | 来源 | ClawHub Slug | 版本 | 备注 |
|-------|------|-------------|------|------|
| `self-improving` | `ivangdavila` | `self-improving` | 1.2.16 | |
| `proactivity` | `ivangdavila` | `proactivity` | 1.0.1 | |
| `agent-browser` | 外部下载 | `agent-browser` | 0.2.0 | |
| `word-docx` | `ivangdavila` | `word-docx` | 1.0.2 | |
| `excel-xlsx` | `ivangdavila` | `excel-xlsx` | 1.0.2 | |
| `humanizer` | `biostartechnology` | `humanizer` | 1.0.0 | |
| `7habits-operations-guide` | 外部下载 | — | — | 内部管理 |
| `aabao-gemini-img2img` | 外部下载 | — | — | 内部管理 |
| `conversation-summarizer` | 外部下载 | — | — | 内部管理 |
| `gog` | 外部下载 | — | — | 内部管理 |
| `inventory-ledger-splitter` | 外部下载 | — | — | 内部管理 |
| `job-hunt-orchestrator` | 外部下载 | — | — | 内部管理 |
| `model-config` | 外部下载 | — | — | 内部管理 |
| `operations-advisor` | 外部下载 | — | — | 内部管理 |
| `unraid-dockerman-xml-deploy` | 外部下载 | — | — | 内部管理 |
| `unraid-xml-generator` | 外部下载 | — | — | 内部管理 |

---

## ClawHub 实际安装状态（截至 2026-04-06）

```
agent-browser   0.2.0
sure-api       1.0.0    ← 自建
word-docx      1.0.2
excel-xlsx     1.0.2
self-improving 1.2.16
proactivity    1.0.1
humanizer     1.0.0
```

> 注：外部的 `vikunja-fast`（tmigone）和 `self-improving-agent`（pskoett）已卸载。`vikunja-task-api`（我们自建）的本地版本存在于 `~/.openclaw/workspace/skills/vikunja-fast/` 目录（v2.5.0），未在 ClawHub 安装列表中。

---

## 发布/更新流程

```bash
# 1. 在 /tmp/openclaw-person-skills 更新文件
# 2. 推送到 GitHub
cd /tmp/openclaw-person-skills
git add -A && git commit -m "feat: ..."
git push

# 3. 发布/更新到 ClawHub
clawhub publish skills/[skill-name] \
  --slug ashanzzz-[slug] \
  --version X.X.X \
  --tags "..." \
  --changelog "..."

# 4. 克隆到本地私人仓库备份
cd /tmp/private-life
git clone https://github.com/ashanzzz/private-life.git
# 手动复制要备份的 skill 文件进去
git push
```

---

## 更新日志

- 2026-04-06：核实全部技能来源，清理孤儿记录（`proactive-agent-skill`、`proactive-agent`、`self-improving-agent`、`vikunja-fast`），确认 `sure-api` 和 `vikunja-task-api` 为自建技能
