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

## 技能清单

### 一、openclaw-person-skills 仓库（已发布到 ClawHub）

| Skill | 来源 | 说明 |
|-------|------|------|
| `deep-research` | **自建** | 2026-04-06 创建，8步研究方法论 |
| `vikunja-task-api` | **自建** | 2026-04-03 创建，Vikunja v2 API |
| `skill-vetter` | **自建** | 2026-04-06 创建，安全审核协议 |
| `unraidclaw` | **Fork 自建** | 2026-04-06 从本地 workspace 复制并发布 |
| `books-growth-advisor` | **自建** | 基于9本管理书的顾问框架 |
| `erpnext-monthly-invoice-export` | **自建** | ERPNext 月度发票导出 |
| `erpnext-invoice-detail-export` | **自建** | ERPNext 发票明细导出 |
| `finance-reconcile-workbook` | **自建** | 财务对账工作簿生成器 |
| `finance-remark-mapping` | **自建** | 财务备注映射 |
| `purchase-wire-transfer-reconcile` | **自建** | 采购电汇对账 |
| `purchase-invoice-classifier` | **自建** | 采购发票分类 |
| `reconcile-output-format` | **自建** | 对账输出格式化 |
| `book-learner` | **自建** | 图书切片阅读与笔记生成 |
| `book-audit` | **自建** | 图书笔记完整性审计 |
| `book-notes-sop` | **自建** | 大任务一次性执行 SOP |
| `repo-structure-manager` | **自建** | 仓库结构治理 |
| `news-tracker` | **自建** | 新闻追踪存档 |

---

### 二、本地 workspace 独有（未发布到公共仓库）

| Skill | 来源 | 说明 |
|-------|------|------|
| `7habits-operations-guide` | **？** | 待确认 |
| `aabao-gemini-img2img` | **外部下载** | aabao Gemini 图生图（用户提供） |
| `agent-browser` | **外部下载** | Agent Browser 自动化 |
| `conversation-summarizer` | **外部下载** | 会话摘要上传 ClawHub |
| `excel-xlsx` | **外部下载** | Excel 操作 |
| `gog` | **外部下载** | 待确认 |
| `humanizer` | **外部下载** | 待确认 |
| `inventory-ledger-splitter` | **外部下载** | 库存账本拆分 |
| `job-hunt-orchestrator` | **外部下载** | 找工作编排 |
| `model-config` | **外部下载** | 模型配置管理 |
| `operations-advisor` | **外部下载** | 运营顾问（引用 books-growth-advisor） |
| `proactivity` | **外部下载** | 主动工作流（用户已确认） |
| `self-improving` | **外部下载** | 自学习（用户已确认） |
| `self-improving-agent` | **外部下载** | 自学习 agent（用户已确认） |
| `sure-api` | **外部下载** | we-promise/sure API |
| `unraid-dockerman-xml-deploy` | **外部下载** | Unraid Docker XML 部署 |
| `unraid-xml-generator` | **外部下载** | Unraid XML 模板生成 |
| `vikunja-fast` | **Fork 自建** | vikunja-task-api 的简化版（用户已确认来自外部） |
| `word-docx` | **外部下载** | Word 操作 |
| `ruijie-noc-donglihu-watch` | **自建** | 锐捷 NOC 监控脚本（TOOLS.md 记录） |

---

## 待用户确认

以下技能我无法确定来源，请帮忙纠正：

- [ ] `7habits-operations-guide` — 来源？
- [ ] `gog` — 来源？
- [ ] `humanizer` — 来源？
- [ ] `operations-advisor` — 是外部下载的还是我们写的？
- [ ] `repo-structure-manager` — 来源？（在 openclaw-person-skills 里，但不确定原始来源）

---

## 已确认外部来源

| Skill | 原始来源 |
|-------|---------|
| `proactivity` | ClawHub / 外部社区 |
| `self-improving` | ClawHub / 外部社区 |
| `self-improving-agent` | ClawHub / 外部社区 |
| `vikunja-fast` | 外部 fork（基于 vikunja-task-api） |

---

## 同步方式说明

| 同步目标 | 内容 | 同步方式 |
|---------|------|---------|
| **本地 workspace** | 所有技能的工作副本 | 实时读写，`~/.openclaw/workspace/skills/` |
| **GitHub 公共仓库** | 公开分享的技能 | `git push` 到 `ashanzzz/openclaw-person-skills` |
| **ClawHub** | 公共技能市场 | `clawhub publish` 发布/更新 |
| **GitHub 私人仓库** | 私人资产备份 | `git push` 到 `ashanzzz/private-life` |

## 同步状态追踪

### 同步到 ClawHub（公共技能市场）

| Skill | ClawHub Slug | 版本 | 状态 |
|-------|--------------|------|------|
| `deep-research` | `ashanzzz-deep-research` | 1.2.0 | ✅ 已发布 |
| `vikunja-task-api` | `ashanzzz-vikunja-task-api` | 2.4.0 | ✅ 已发布 |
| `skill-vetter` | `ashanzzz-skill-vetter` | 1.2.0 | ✅ 已发布 |
| `unraidclaw` | `ashanzzz-unraidclaw` | 1.2.0 | ✅ 已发布 |
| `books-growth-advisor` | — | — | ⏳ 待发布 |
| `erpnext-monthly-invoice-export` | — | — | ⏳ 待发布 |
| `erpnext-invoice-detail-export` | — | — | ⏳ 待发布 |
| `finance-reconcile-workbook` | — | — | ⏳ 待发布 |
| `finance-remark-mapping` | — | — | ⏳ 待发布 |
| `purchase-wire-transfer-reconcile` | — | — | ⏳ 待发布 |
| `purchase-invoice-classifier` | — | — | ⏳ 待发布 |
| `reconcile-output-format` | — | — | ⏳ 待发布 |
| `book-learner` | — | — | ⏳ 待发布 |
| `book-audit` | — | — | ⏳ 待发布 |
| `book-notes-sop` | — | — | ⏳ 待发布 |
| `repo-structure-manager` | — | — | ⏳ 待发布 |
| `news-tracker` | — | — | ⏳ 待发布 |

### 同步到 GitHub 公共仓库（openclaw-person-skills）

- **推送**：`git push` 到 `https://github.com/ashanzzz/openclaw-person-skills`
- **状态**：所有自建技能均已在此仓库

### 同步到 GitHub 私人仓库（private-life）

- **推送**：`git push` 到 `https://github.com/ashanzzz/private-life`
- **内容**：私人技能备份（如 deep-research SKILL.md）
- **状态**：私人资产按需备份

### 本地 workspace（~/.openclaw/workspace/skills/）

- 所有技能的工作副本均在此
- 自建 + 外部下载技能混合存放
- **重要**：本地有但不在 `openclaw-person-skills` 的技能 = 外部下载或私人技能

---

## 发布/更新流程

```bash
# 1. 在本地 /tmp/openclaw-person-skills 更新文件

# 2. 推送到 GitHub
cd /tmp/openclaw-person-skills
git add -A
git commit -m "feat: ..."
git push

# 3. 发布/更新到 ClawHub
clawhub publish skills/[skill-name] --slug ashanzzz-[slug] --version X.X.X --tags "..." --changelog "..."
```

---

## 更新日志

- 2026-04-06：初建，根据 commit 历史和对话记录初步判断来源，标注待确认项
