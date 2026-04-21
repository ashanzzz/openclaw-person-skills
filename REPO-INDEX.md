# Repository Index

最后更新：2026-04-08

## 1) Repository Policy

仅保留：
- `skills/` 下的技能与依赖文件
- 仓库说明文档

不保留：
- 运行数据
- 电子书原始文件
- 临时切片与缓存

## 2) Skills

| Skill | Purpose | 来源 |
|---|---|
| `skills/erpnext-account-report` | ERPNext 账单导出：GL→PE→PI→物料自动勾稽，每行一个物料明细，含规格/单价/发票号/付款方式 | 本地自建 |
| `skills/erpnext-invoice-detail-export` | ERPNext 发票明细导出：按发票号导出含规格型号/备注的明细 | 本地自建 |
| `skills/erpnext-monthly-invoice-export` | ERPNext 月度发票导出：按公司+月份导出采购发票，含未付款标记 | 本地自建 |
| `skills/business-analysis` | 商业分析：四轮验证+十二维分析+数据源URL+报告模板 | 本地自建 |
| `skills/books-growth-advisor` | 基于9本管理书回答职业发展/工厂/管理/人际问题 | 本地自建 |
| `skills/book-learner` | 图书切片阅读与笔记生成流程 | 本地自建 |
| `skills/book-audit` | 图书笔记完整性复核与修复 | 本地自建 |
| `skills/book-notes-sop` | 九本书大任务一次性执行 SOP | 本地自建 |
| `skills/deep-research` | 深度研究方法论：8步研究流程+4级来源可信度+多源交叉核实 | 本地自建 |
| `skills/finance-reconcile-workbook` | 财务对账工作簿：A/B双口径工作表 | 本地自建 |
| `skills/finance-remark-mapping` | 财务备注映射：银行摘要与发票/凭证备注自动匹配 | 本地自建 |
| `skills/news-tracker` | 新闻跟踪技能 | 本地自建 |
| `skills/purchase-invoice-classifier` | 采购发票分类 | 本地自建 |
| `skills/purchase-wire-transfer-reconcile` | 采购电汇对账 | 本地自建 |
| `skills/reconcile-output-format` | 对账输出格式化 | 本地自建 |
| `skills/skill-creator` | OpenClaw Skill 创建/编辑/审核完整指南 | 本地自建 |
| `skills/skill-vetter` | 安装外部技能前必做的 RED FLAGS 安全审核 | 本地自建 |
| `skills/vikunja-task-api` | 完整 Vikunja v2 API 集成：项目/任务/标签/团队/视图/评论 | 本地自建 |
| `skills/repo-structure-manager` | 仓库目录治理、清理、发布边界控制 | 本地自建 |
| `skills/work-tracker` | 主动工作追踪：未完成/已完成/跟进/预判，基于 Vikunja + Hermes cron | 本地自建 |

## 3) Runtime Data Placement (outside this repo)

运行产物请放到本地工作目录或外部存储，不提交到本仓库。
