---
name: skill-creator
description: 创建、编辑、改进或审核 OpenClaw AgentSkill。触发场景：用户要求"创建一个 skill"、"写一个技能"、"帮我新建技能"、"改进这个 skill"、"审核 skill"、"整理 skill"、"完善技能说明"。同时用于：skill 目录结构调整、文件迁移（移动到 references/ 或 scripts/）、移除过时内容、验证是否符合 AgentSkills 规范。
---

# Skill Creator 🛠️

创建高质量 OpenClaw AgentSkill 的完整指南。

## When to Use This Skill

- 用户要求**新建**一个 skill（从零开始）
- 用户要求**改进**现有 skill（补结构、加示例、删冗余）
- 用户要求**审核** skill（检查规范符合度、安全性、完整性）
- 用户要求**整理** skill（重排目录、加 references/、加 constraints）
- 用户要求**发布** skill（上传 ClawHub / GitHub）

---

## 一、Skills 是什么

Skills 是模块化、自包含的能力扩展包，通过提供**专业领域知识、工作流程和工具集成**来增强 Agent 的能力。

每个 Skill 就是一个文件夹，至少包含：

```
skill-name/
├── SKILL.md          ← 必需（能力定义 + 使用说明）
├── scripts/          ← 可选（可执行脚本）
├── references/       ← 可选（按需加载的参考资料）
└── assets/          ← 可选（模板、图片等输出型资源）
```

---

## 二、核心原则

### 原则 1：简洁是金

Context Window 是公共资源。Agent 需要同时承载：系统提示、对话历史、其他 Skills 的元数据，以及当前用户请求。

**默认假设：Agent 已经足够聪明。** 只添加 Agent 本身不具备的内容。逐条审视："这条指令 Agent 真的需要吗？这段话值得花多少 tokens？"

优先用简洁示例替代冗长解释。

### 原则 2：渐进式披露（Progressive Disclosure）

三级加载结构，管理 context 高效利用：

| 层级 | 内容 | 加载时机 | 篇幅上限 |
|------|------|---------|---------|
| 第一级 | `name` + `description` | 始终在 context | ~100 words |
| 第二级 | SKILL.md 正文 | Skill 触发后 | **<500 行** |
| 第三级 | references/ / scripts/ | 按需执行/读取 | 无限制 |

**关键原则：**< 500 行的 SKILL.md 是目标，超出则拆分到 references/ 文件。

### 原则 3：自由度匹配任务脆弱度

| 自由度 | 形式 | 适用场景 |
|--------|------|---------|
| 高 | 纯文本指令 | 多路径有效、依赖上下文判断 |
| 中 | 伪代码 / 参数化脚本 | 有推荐模式、可接受一定变化 |
| 低 | 固定脚本、少参数 | 脆弱易错、一致性关键 |

### 原则 4：示例优先于说明

实测经验：**Examples 章节对质量提升最显著**。好/坏对比示例比任何文字说明都有效。

---

## 三、SKILL.md 标准结构

每个 SKILL.md 必须包含：

### 3.1 Frontmatter（必需）

```yaml
---
name: skill-name          # 小写字母、数字、连字符，≤64字符
description: 简短描述（做什么 + **何时触发**，触发条件放这里，不是正文）
---
```

**description 写法规范（最重要）：**
- 必须包含"做什么"**和**"何时用"两部分
- 所有触发信息放 description，不放正文（正文只在触发后才加载）
- 不能包含 `<` 或 `>` 符号
- 上限 1024 字符

**反面例子：**
```yaml
description: ERPNext 发票导出技能。
```

**正面例子：**
```yaml
description: ERPNext 月度发票导出。触发条件：(1) 用户要求"导出某公司某月发票"；
(2) 用户要求"查某月未付款发票"；(3) 用户提供公司名+月份组合时。
```

### 3.2 正文结构（推荐顺序）

```markdown
# Skill Name

## When to Use This Skill
（触发场景：用户在什么情况下应该调用这个 skill）

## Context / 背景
（Agent 需要知道的专业领域知识，具体到你的场景）

## Instructions / 执行步骤
（分步流程，每步有明确的质量标准）

## Constraints / 约束
（禁止事项：绝对不能做什么，来自真实失败经验）

## Examples（推荐）
（好/坏输出对比示例，对质量提升最显著）
```

### 3.3 禁止事项

以下文件**不应**出现在 Skill 目录中（它们是给人类看的，不是给 Agent 用的）：
- README.md
- INSTALLATION_GUIDE.md
- CHANGELOG.md
- QUICK_REFERENCE.md

---

## 四、创建流程（六步）

### Step 1：理解需求（带具体示例）

不要急着写，先问清楚：
- "这个 skill 主要用来做什么？"
- "能给我 1-2 个具体使用场景吗？"
- "用户会怎么描述这个需求？（触发原话）"
- "这个 skill 需要调用哪些工具或 API？"

### Step 2：规划 Skill 内容

分析每个使用场景，确定需要哪些资源：

| 资源类型 | 什么时候用 | 例子 |
|---------|-----------|------|
| `scripts/` | 需要确定性执行、反复重写相同代码 | PDF 旋转脚本、API 调用封装 |
| `references/` | 需要按需加载的详细文档 | API 文档、数据库 schema、公司政策 |
| `assets/` | 需要复制到输出中的文件 | 模板、Logo、字体 |

### Step 3：初始化 Skill 目录

```bash
cd <workspace>/skills
python3 <skill-creator>/scripts/init_skill.py <skill-name> \
  --path . --resources scripts,references
```

或者手动创建：
```bash
mkdir -p skills/<skill-name>/{scripts,references}
touch skills/<skill-name>/SKILL.md
```

### Step 4：编写 SKILL.md

**Frontmatter 写法（两条规则）：**
1. `name`：小写 + 连字符，≤64 字符
2. `description`：**"做什么" + "何时触发"（触发条件放这里）**，不是正文

**正文写法：**
- 用**祈使句**（"Do X", "Don't do Y"）
- 每步有**明确质量标准**
- 包含真实失败经验（Constraints 章节）

**参考现有好范例：**
- `skill-vetter` — 清晰的风险分级 + 枚举式检查项
- `erpnext-monthly-invoice-export` — 具体 API 端点 + curl 示例（注意脱敏）

### Step 5：打包验证

```bash
# 验证格式
python3 <skill-creator>/scripts/quick_validate.py <skill-path>

# 打包成分发文件
python3 <skill-creator>/scripts/package_skill.py <skill-path> [output-dir]
```

验证通过标准：
- Frontmatter 有 `name` + `description`
- `name` 符合小写连字符规范
- `description` 不含 `<` `>`，≤1024 字符
- SKILL.md 存在且非空

### Step 6：发布

**ClawHub 发布：**
```bash
cd <skill-directory>
clawhub publish
# 或指定路径：
clawhub publish <skill-path>
```

**GitHub 发布（公共仓库）：**
1. 建仓库：`gh repo create ashanzzz/skill-<name> --public --source . --push`
2. 在 ClawHub 填入 GitHub 仓库链接（可选）

---

## 五、Workspace 规范（本 Skill 自用规则）

创建发布到 ClawHub 的 Skill 时，**强制遵守**：

### 5.1 环境变量占位符

**禁止**在 SKILL.md 或代码中硬编码具体值。
使用下述通配符格式，运行时替换：

| 真实值 | 占位符格式 | 例子 |
|--------|-----------|------|
| API Base URL | `{{SERVICE_BASE_URL}}` | `{{ERP_BASE_URL}}` |
| API Token | `{{ERP_API_TOKEN}}` | （不暴露具体值） |
| 主机地址 | `{{SYNOLOGY_HOST_LAN}}` | `{{SYNOLOGY_HOST_LAN}}:5006` |
| 文件路径 | `{{DSM_WEBDAV_ROOT}}` | `{{DSM_WEBDAV_ROOT}}/opencode/` |
| 数据库 | `{{POSTGRES_HOST}}` | `{{POSTGRES_HOST}}:5432` |

### 5.2 MIT-0 许可证

所有公开的 Skill 必须使用 **MIT-0**（免费使用、修改、分发，无需署名）：
```yaml
license: MIT-0
```

### 5.3 触发原话示例

SKILL.md 的 description 应包含真实触发原话：
```yaml
description: 触发条件：用户说"帮我新建一个 skill"、"创建技能"、"author a skill"、
"生成 Unraid XML 模板"、"写 Docker 模板"时使用。
```

### 5.4 目录结构规范

```
skill-name/
├── SKILL.md              ← 唯一入口，≤500 行
├── scripts/              ← 可执行脚本（Python/Bash）
│   ├── init_skill.py     ← 初始化脚本（如需要）
│   └── validate_skill.py ← 验证脚本（如需要）
├── references/           ← 按需加载的参考资料
│   └── *.md              ← 按主题拆分
└── assets/              ← 输出型资源（模板等）
```

### 5.5 分发包格式

ClawHub 接受两种分发：
- **.skill 文件**（zip 压缩包，推荐）
- **直接目录**（ClawHub 从目录读取）

```bash
# 生成分发包
python3 <skill-creator>/scripts/package_skill.py <skill-path>
```

---

## 六、好 Skill vs 差 Skill 对比

| 维度 | 差 Skill | 好 Skill |
|------|---------|---------|
| description | "这是一个 Excel 技能" | "创建/编辑 Excel，支持公式/格式/多Sheet。触发：用户提供 .xlsx 文件、要求生成报表、要求格式化。" |
| 正文结构 | 混杂一堆命令 | 清晰的 When to Use → Steps → Constraints → Examples |
| 示例 | 无 | 有好/坏对比，知道 Agent 真正需要什么 |
| 长度 | 1000+ 行全部堆 SKILL.md | ≤500 行，references/ 承接详细文档 |
| 约束 | 无 | 有真实失败经验转化来的禁止规则 |

---

## 七、快速检查清单

创建或审核 Skill 时，逐项确认：

- [ ] `name` 是小写字母+数字+连字符？
- [ ] `description` 有"做什么"+"何时触发"两部分？
- [ ] `description` 不含 `<` `>` 符号？
- [ ] `description` ≤1024 字符？
- [ ] `license: MIT-0`？（公开发布时）
- [ ] 正文有 `When to Use This Skill` 章节？
- [ ] 正文有 `Constraints` 章节（禁止事项）？
- [ ] 有 `Examples` 章节（推荐）？
- [ ] SKILL.md 正文 ≤500 行？
- [ ] 环境变量用 `{{VAR_NAME}}` 占位符？
- [ ] 没有 README.md / CHANGELOG.md 等辅助文档？
- [ ] 验证脚本通过（`quick_validate.py`）？
