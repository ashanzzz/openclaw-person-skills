# Repository Index

最后更新：2026-04-03

## 1) Skills

| Skill | Purpose |
|---|---|
| `skills/book-learner` | 图书切片阅读与笔记生成 |
| `skills/book-audit` | 图书笔记完整性复核与修复 |
| `skills/book-notes-sop` | 九本书大任务的一次性执行 SOP |
| `skills/books-growth-advisor` | 基于九本书的职业/工厂/管理/沟通综合咨询 |
| `skills/repo-structure-manager` | 仓库目录治理、合并、清理、发布边界控制 |
| `skills/erpnext-invoice-detail-export` | ERPNext 发票明细导出 |
| `skills/erpnext-monthly-invoice-export` | ERPNext 月度发票导出 |
| `skills/finance-reconcile-workbook` | 财务对账模板与工作簿处理 |
| `skills/finance-remark-mapping` | 财务备注映射 |
| `skills/news-tracker` | 新闻跟踪与归档 |
| `skills/purchase-invoice-classifier` | 采购发票分类 |
| `skills/purchase-wire-transfer-reconcile` | 采购电汇对账 |
| `skills/reconcile-output-format` | 对账输出格式化 |
| `skills/vikunja-task-api` | Vikunja API 任务管理 |

## 2) Knowledge / Outputs

- `kb/books-notes/`：九本书笔记、master、meta、复核报告
- `kb/news-tracker/`：新闻追踪运行输出（daily/topics）

## 3) Publish Policy

- ✅ 可发布：技能文件、笔记文件、报告文件
- ❌ 不发布：EPUB、原始切片（`slice_*.md`）

## 4) Cleanup actions completed

1. 统一技能目录到 `skills/`。
2. 清理冗余备份文件（`*.bak*`）。
3. 将运行数据从 skill 目录迁移到 `kb/`。
4. 新增仓库治理技能 `repo-structure-manager`。
5. 新增九本书咨询技能 `books-growth-advisor`。
