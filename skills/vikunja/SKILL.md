---
name: Vikunja Task Manager
slug: vikunja
version: 1.2.0
description: "Vikunja 个人任务管理系统集成。每次拉取任务后自动存本地缓存（~/.vikunja-cache.json），并与上次缓存对比，报告新增/完成/过期/删除的任务变化。配合 work-tracker 实现主动追踪。"
metadata:
  tags: [vikunja, task-management, api-integration, local-cache, diff-tracking]
  hermes:
    tools_used: [terminal, send_message]
    configPaths: [~/.vikunja-cache.json, /opt/data/secrets.txt]
---

## 核心功能

每次调用 `fetch` 或 `nudge` 时：
1. 从 Vikunja API 拉取最新任务列表
2. 读取本地缓存 `~/.vikunja-cache.json`
3. 对比差异，报告变化
4. 更新本地缓存

---

## API 信息

```
Base URL: http://192.168.8.11:3456/api/v1
Token: tk_3f7b39dc6cf65e27e9a194ab8278db6f335785bd
```

Token 读取自 `/opt/data/secrets.txt` 的 `VIKUNJA_API_KEY`。

---

## 脚本

### `fetch` — 拉取 + 缓存 + 对比

```bash
python3 /opt/data/skills/productivity/vikunja/scripts/fetch.py
```

**输出格式：**
```
📋 Vikunja 任务状态 — 2026-04-21 09:15 北京时间

🔴 已过期（3）：
  #61 车辆年检（截止 2026-04-18）
  #88 油卡充值（截止 2026-04-05）
  #89 信用卡500元年费（截止 2026-04-10）

✅ 新完成（since 2026-04-20 18:32）：
  #36 Updated-back
  #37 确定接口形态：Gradio WebUI 或 FastAPI

🆕 新增任务（2）：
  #N title...

⚪ 进行中无截止日期（18）：
  #38 ... #90 ...

📁 缓存已更新：~/.vikunja-cache.json
```

---

### `nudge` — 主动推送格式

```bash
python3 /opt/data/skills/productivity/vikunja/scripts/fetch.py nudge
```

**输出格式：** 同上，但更简洁，适合 Telegram 推送。

---

### `list` — 仅列出活跃任务

```bash
python3 /opt/data/skills/productivity/vikunja/scripts/fetch.py list
```

---

### `overdue` — 仅显示过期任务

```bash
python3 /opt/data/skills/productivity/vikunja/scripts/fetch.py overdue
```

---

### `snapshot` — 手动保存基准线

```bash
python3 /opt/data/skills/productivity/vikunja/scripts/fetch.py snapshot
```

---

## 本地缓存格式

`~/.vikuncha-cache.json` 结构：

```json
{
  "updated_at": "2026-04-21T09:15:00+08:00",
  "total_count": 27,
  "tasks": {
    "36": {"title": "Updated-back", "done": true, "done_at": "2026-04-20"},
    "37": {"title": "确定接口形态：Gradio WebUI 或 FastAPI", "done": true, "done_at": "2026-04-20"},
    "38": {"title": "...", "done": false, "due_date": null},
    ...
  },
  "diff_from_previous": {
    "new": [],
    "completed": ["36", "37"],
    "deleted": [],
    "newly_overdue": []
  }
}
```

---

## 新对话开始流程

每次新对话开始时，自动执行以下步骤（不用等用户问）：

```
1. 读取 ~/.vikunja-cache.json（上次缓存）
2. 调用 Vikunja GET /tasks 拉取最新列表
3. 对比：
   - newly_completed = 上次未完成但本次已完成
   - newly_overdue = 上次未过期但本次已过期
   - new_tasks = 本次有但上次没有的任务
   - deleted = 上次有但本次没有的任务
4. 若有任何变化 → 主动格式化报告给用户
5. 更新 ~/.vikunja-cache.json
```

---

## API 端点参考

| 端点 | 方法 | 说明 |
|------|------|------|
| `/tasks` | GET | 获取所有任务（`?per_page=100`） |
| `/tasks/{id}` | GET | 获取单个任务 |
| `/tasks` | POST | 创建任务 |
| `/tasks/{id}` | PUT | 更新任务（done/label/due_date） |
| `/tasks/{id}/position` | POST | 更新任务位置 |
| `/tasks/bulk` | POST | 批量更新 |

---

## 配置

Token 从 `/opt/data/secrets.txt` 读取（`VIKUNJA_API_KEY`）。

若需更换 API 地址或 token，直接编辑 `/opt/data/secrets.txt`。
