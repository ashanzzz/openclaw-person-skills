# openclaw-person-skills

阿山的个人 OpenClaw Skills 仓库（已整理版）。

## 当前仓库结构

```text
skills/                 # 全部技能（统一入口）
kb/books-notes/         # 书籍笔记与复核报告
kb/news-tracker/        # 新闻追踪运行数据（非技能文件）
README.md
REPO-INDEX.md
.gitignore
```

## 技能目录（统一在 `skills/`）

- `book-learner`
- `book-audit`
- `book-notes-sop`
- `books-growth-advisor`
- `repo-structure-manager`
- `erpnext-invoice-detail-export`
- `erpnext-monthly-invoice-export`
- `finance-reconcile-workbook`
- `finance-remark-mapping`
- `news-tracker`
- `purchase-invoice-classifier`
- `purchase-wire-transfer-reconcile`
- `reconcile-output-format`
- `vikunja-task-api`

## 关键规则

1. 技能只放 `skills/`，不再在仓库根目录散落 skill 文件夹。
2. 图书流程仅发布笔记与技能：
   - 发布：`master.md`、`slice_*_n.md`、`meta.json`、复核报告
   - 不发布：EPUB、原始 `slice_*.md`
3. 运行数据与技能资源分离（如 `kb/news-tracker/`）。

详细目录见：`REPO-INDEX.md`
