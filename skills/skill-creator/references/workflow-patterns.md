# OpenClaw Skill 工作流模式参考

本文档提供创建 Skill 时的常用模式参考。

---

## 模式一：顺序工作流

适用于：步骤固定、顺序执行的场景。

```markdown
## 执行步骤

### Step 1: 准备
[做什么 + 验证方法]

### Step 2: 执行核心操作
[具体命令/API 调用]

### Step 3: 校验结果
[如何确认成功/失败]
```

---

## 模式二：任务分支

适用于：同一 Skill 支持多种操作类型。

```markdown
## 支持的操作

### 类型 A：导出
[步骤]

### 类型 B：导入
[步骤]

### 类型 C：查询
[步骤]
```

---

## 模式三：参考文件导航

适用于：内容多，必须拆分到 references/。

SKILL.md 中：
```markdown
## 详细参考

- **API 文档**: 见 `references/api.md`
- **常见错误**: 见 `references/errors.md`
- **示例**: 见 `references/examples.md`
```

references/api.md 中：
```markdown
# API 参考

## 认证
[详细说明]

## 端点列表
[完整列表]
```

---

## 模式四：好/坏对比示例

```markdown
## Examples

### ✅ 正确示范
用户说："帮我导出吉众3月发票"
Agent 做法：[正确步骤]
输出：[符合标准的 Excel]

### ❌ 错误示范
用户说："导出发票"
Agent 做法：[踩坑操作]
结果：[格式错误/缺少字段]
原因：没有确认公司和月份
```
