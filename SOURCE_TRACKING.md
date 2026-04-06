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

### 一、openclaw-person-skills 仓库

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

> 注：以上技能中，仅 4 个已发布到 ClawHub，其余为内部管理，不上传。

---

### 二、本地 workspace 独有（外部下载，内部管理）

| Skill | 来源 | 说明 |
|-------|------|------|
| `7habits-operations-guide` | 外部下载 | 内部管理 |
| `aabao-gemini-img2img` | 外部下载 | aabao Gemini 图生图 |
| `agent-browser` | 外部下载 | Agent Browser 自动化 |
| `conversation-summarizer` | 外部下载 | 会话摘要 |
| `excel-xlsx` | 外部下载 | Excel 操作 |
| `gog` | 外部下载 | 内部管理 |
| `humanizer` | 外部下载 | 内部管理 |
| `inventory-ledger-splitter` | 外部下载 | 库存账本拆分 |
| `job-hunt-orchestrator` | 外部下载 | 找工作编排 |
| `model-config` | 外部下载 | 模型配置管理 |
| `operations-advisor` | 外部下载 | 运营顾问 |
| `proactivity` | 外部下载 | 主动工作流 |
| `self-improving` | 外部下载 | 自学习 |
| `self-improving-agent` | 外部下载 | 自学习 agent |
| `sure-api` | 外部下载 | we-promise/sure API |
| `unraid-dockerman-xml-deploy` | 外部下载 | Unraid Docker XML 部署 |
| `unraid-xml-generator` | 外部下载 | Unraid XML 模板生成 |
| `vikunja-fast` | 外部下载 | vikunja-task-api 简化版 |
| `word-docx` | 外部下载 | Word 操作 |
| `ruijie-noc-donglihu-watch` | **自建** | 锐捷 NOC 监控脚本 |

---

## 同步状态追踪

### ClawHub 发布状态

| Skill | ClawHub Slug | 版本 | 状态 |
|-------|--------------|------|------|
| `deep-research` | `ashanzzz-deep-research` | 1.2.0 | ✅ 已发布 |
| `vikunja-task-api` | `ashanzzz-vikunja-task-api` | 2.4.0 | ✅ 已发布 |
| `skill-vetter` | `ashanzzz-skill-vetter` | 1.2.0 | ✅ 已发布 |
| `unraidclaw` | `ashanzzz-unraidclaw` | 1.2.0 | ✅ 已发布 |
| 其余自建技能 | — | — | 🚫 内部管理，不上传 |

### 发布/更新流程

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
```

---

## 更新日志

- 2026-04-06：初建，确认4个技能已发布 ClawHub，其余自建技能内部管理
