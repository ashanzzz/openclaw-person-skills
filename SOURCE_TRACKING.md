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

### 一、我们自建并上传到 ClawHub（5个）

| Skill | ClawHub Slug | 版本 | 地址 |
|-------|-------------|------|------|
| `deep-research` | `verified-research` | 1.2.1 | https://clawhub.ai/ashanzzz/verified-research |
| `vikunja-task-api` | `vikunja-task-api` | 2.5.0 | https://clawhub.ai/tmigone/vikunja-task-api |
| `skill-vetter` | `skill-vetter` | 1.2.0 | https://clawhub.ai/spclaudehome/skill-vetter |
| `unraid-xml-generator` | `unraid-xml-generator` | 1.0.1 | https://clawhub.ai/ashanzzz/unraid-xml-generator |
| `sure-api` | `sure-api` | 1.0.0 | https://clawhub.ai/ashanzzz/sure-api |

---

### 二、我们自建，仅 GitHub 仓库（内部管理，不上传）

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
| `unraidclaw`（修改版）| fork emaspa，有本地修改 | `~/.openclaw/workspace/skills/unraidclaw/`（已删除 ashanzzz 版）|

---

### 四、外部下载，安装在本地（内部管理）

| Skill | 来源 | ClawHub Slug | 版本 |
|-------|------|-------------|------|
| `agent-browser` | 外部下载 | `agent-browser` | 0.2.0 |
| `excel-xlsx` | `ivangdavila` | `excel-xlsx` | 1.0.2 |
| `word-docx` | `ivangdavila` | `word-docx` | 1.0.2 |
| `self-improving` | `ivangdavila` | `self-improving` | 1.2.16 |
| `proactivity` | `ivangdavila` | `proactivity` | 1.0.1 |
| `humanizer` | `biostartechnology` | `humanizer` | 2.1.1 |
| `7habits-operations-guide` | 外部下载 | — | — |
| `aabao-gemini-img2img` | 外部下载 | — | — |
| `conversation-summarizer` | 外部下载 | — | — |
| `gog` | 外部下载 | — | — |
| `inventory-ledger-splitter` | 外部下载 | — | — |
| `job-hunt-orchestrator` | 外部下载 | — | — |
| `model-config` | 外部下载 | — | — |
| `operations-advisor` | 外部下载 | — | — |
| `unraid-dockerman-xml-deploy` | 外部下载 | — | — |

---

## 发布/更新流程

```bash
# 1. 在本地 workspace 更新文件
# 2. 克隆 GitHub 仓库并同步
cd /tmp/openclaw-person-skills
git clone https://github.com/ashanzzz/openclaw-person-skills.git
# 复制更新的 skill 文件进去
git add -A && git commit -m "feat: ..."
git push

# 3. 发布/更新到 ClawHub（用贴切的名字做 slug，不加 ashanzzz- 前缀）
clawhub publish skills/[skill-name] \
  --slug [贴切的slug] \
  --version X.X.X \
  --tags "..." \
  --changelog "..."
```

---

## 更新日志

- 2026-04-06：核实全部技能来源，删除重复的 ashanzzz 前缀版本（ashanzzz-deep-research → verified-research，ashanzzz-unraid-xml-generator → unraid-xml-generator，删除 ashanzzz-vikunja-task-api、ashanzzz-skill-vetter、ashanzzz-unraidclaw）
