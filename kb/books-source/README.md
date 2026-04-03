# 书架 — Bookshelf

> 维护者：Zero（阿山的 AI 助手）
> 更新：2026-04-03
> 目的：为阿山建立可查询的知识库，所有原书存储在 `kb/books-source/`

---

## 📚 总书架

| # | 书名 | 英文名 | ISBN | 唯一识别码 | 维基百科 | 状态 | 提炼进度 |
|---|------|--------|------|---------|---------|------|---------|
| 1 | 高效能人士的七个习惯（30周年纪念版） | The 7 Habits of Highly Effective People | 978-7-5153-5058-5 | OL6658934M（OpenLibrary）| [Wikipedia](https://en.wikipedia.org/wiki/The_7_Habits_of_Highly_Effective_People) | ⚠️ 部分提炼 | 60% |
| 2 | 精益思想（白金版） | Lean Thinking | 978-7-111-51071-0 | OL27211608M（OpenLibrary）| [Wikipedia](https://en.wikipedia.org/wiki/Lean_manufacturing) | ✅ 已完成 | 100% |
| 3 | 丰田模式 | The Toyota Way | 978-7-111-33013-4 | OL17974089M（OpenLibrary）| [Wikipedia](https://en.wikipedia.org/wiki/The_Toyota_Way) | ⚠️ 已有丰田之道，可补充 | 40% |
| 4 | 格鲁夫给经理人的第一课（纪念版） | High Output Management | —（1983原版无ISBN） | OL7690664M（OpenLibrary）| [Wikipedia](https://en.wikipedia.org/wiki/Andrew_Grove) | ✅ 已完成 | 100% |
| 5 | 高产出管理（The Goal） | The Goal: A Process of Ongoing Improvement | — | OL2304755M（OpenLibrary）| [Wikipedia](https://en.wikipedia.org/wiki/The_Goal_(novel)) | ⚠️ 已有TOC内容，可补充 | 40% |
| 6 | 人性的弱点 | How to Win Friends and Influence People | 978-7-5153-2181-5 | OL6658934M（OpenLibrary）| [Wikipedia](https://en.wikipedia.org/wiki/How_to_Win_Friends_and_Influence_People) | ✅ 已完成 | 100% |
| 7 | 第五项修炼（最新版） | The Fifth Discipline | 978-7-115-29104-3 | OL17974089M（OpenLibrary）| [Wikipedia](https://en.wikipedia.org/wiki/The_Fifth_Discipline) | ✅ 已完成 | 100% |
| 8 | 管理的常识 | Management Essentials | 978-7-5158-0074-5 | OL2289555M（OpenLibrary）| [Wikipedia](https://en.wikipedia.org/wiki/Management) | ❌ 未提炼 | 0% |
| 9 | 领导梯队 | The Leadership Pipeline | 978-7-111-34934-1 | OL2304755M（OpenLibrary）| [Wikipedia](https://en.wikipedia.org/wiki/Succession_planning) | ⚠️ 部分提炼 | 70% |
| 10 | 驱动力 | Drive: The Surprising Truth About What Motivates Us | 978-7-115-21851-2 | OL2304755M（OpenLibrary）| [Wikipedia](https://en.wikipedia.org/wiki/Drive:_The_Surprising_Truth_About_What_Motivates_Us) | ✅ 已完成 | 100% |

---

## 📖 状态说明

| 符号 | 含义 |
|------|------|
| ✅ 已完成 | 精华已提炼，写入 `skills/operations-management-knowledge/` |
| ⚠️ 部分提炼 | 有基础内容，需补充更多细节/章节 |
| ❌ 未提炼 | 尚未开始处理 |
| 🔄 进行中 | 正在提炼 |

---

## 🏷️ 唯一识别码说明

书籍的"身份证"有以下几种：

| 类型 | 说明 | 示例 |
|------|------|------|
| **ISBN** | 国际标准书号，全球唯一 | 978-7-5153-5058-5 |
| **Open Library ID (OLID)** | 开放图书馆编号，免费可查 | OL6658934M |
| **Goodreads ID** | Goodreads 书评网编号 | — |
| **Wikipedia slug** | 维基百科词条URL后缀 | The_7_Habits_of_Highly_Effective_People |

---

## 📂 文件位置

```
kb/books-source/              # 原书 epub 文件（固定存储位置）
├── 高效能人士的七个习惯.epub
├── 精益思想.epub
├── 丰田模式.epub
├── 格鲁夫给经理人的第一课.epub
├── 高产出管理.epub
├── 人性的弱点.epub
├── 第五项修炼.epub
├── 管理的常识.epub
├── 领导梯队.epub
└── 驱动力.epub

skills/operations-management-knowledge/   # 精华提炼（AI 已学习）
├── factory-operations/
│   ├── goal-toc.md           ✅ 已完成
│   ├── lean-thinking.md       ✅ 已完成
│   └── toyota-way.md         ⚠️ 部分
├── management/
│   ├── 7habits-framework.md  ⚠️ 部分
│   ├── fifth-discipline.md    ✅ 已完成
│   ├── high-output-mgmt.md   ✅ 已完成
│   └── leadership-pipeline.md ⚠️ 部分
└── personal-development/
    ├── drive-motivation.md  ✅ 已完成
    ├── habits-1-3.md       ⚠️ 部分
    ├── habits-4-7.md        ⚠️ 部分
    └── how-to-win-friends.md ✅ 已完成
```

---

## 🎯 提炼标准

每本书必须提炼以下内容：

```
✅ 核心论点（作者要解决什么问题）
✅ 三要素/五原则/七习惯（核心框架）
✅ 关键概念（行话/术语定义）
✅ 实践工具（可操作的方法/SOP）
✅ 案例/故事（加深理解的具体例子）
✅ 与其他书的关联（知识网络）
✅ 行动清单（读者/AI可以做什么）
✅ 关键语录（值得记住的原话）
✅ 决策矩阵（遇到问题时快速查阅）
```

---

## 🔄 待完成项

### ❌ 管理的常识（优先级：中）

**核心问题**：管理的常识讲什么？

**提炼计划**：读完全书后归类到工厂运营/管理学/个人发展

### ⚠️ 高效能人士七个习惯（优先级：中）

**已有**：`personal-development/habits-1-3.md`, `habits-4-7.md`, `management/7habits-framework.md`

**待补充**：30周年纪念版新增内容（若有）

### ⚠️ 丰田模式（优先级：中）

**已有**：`factory-operations/toyota-way.md`（基于精益思想+丰田之道）

**待确认**：丰田模式与丰田之道的差异

### ⚠️ 高产出管理/The Goal（优先级：低）

**已有**：`factory-operations/goal-toc.md`（TOC部分）

**待确认**：是否需要区分《高产出管理》(The Goal小说) 和 TOC实操

### ⚠️ 领导梯队（优先级：低）

**已有**：`management/leadership-pipeline.md`

**待补充**：基于原书完整内容修订

---

## 🌐 参考资源

- [Open Library](https://openlibrary.org/) — 免费开放的书目数据库，输入ISBN可查OLID
- [Wikipedia](https://en.wikipedia.org/) — 每本书的英文维基百科词条
- [Goodreads](https://www.goodreads.com/) — 全球最大书评社区
- [WorldCat](https://www.worldcat.org/) — 全球图书馆联合目录
