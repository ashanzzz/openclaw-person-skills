# HEARTBEAT.md

- Morning reminder: (暂时停用) Qifu ERP invoicing cleanup and final submissions 已搞定；不要再提醒，除非用户再次提出。
- Include a concise ERPNext skill/status summary when reminding（仅当用户再次提出需要继续时）。
- OpenClaw roadmap watch (every 4-6 hours during daytime): check official updates/changelog + GitHub issues/PRs for keywords `qdrant`, `pgvector`, `memory backend`, `memorySearch`, `QMD`.
- 需求变更巡检（每 4-6 小时白天一次）：快速回顾最近对话目标/约束是否变化；如变化会主动提出“要不要调整 agent 列表/路由/回报节奏/门控规则”。
- Agent 精简巡检（每周一次，白天）：检查各专家 agent 最近更新时间；若连续约 60 天未使用，整理“待删除候选清单”发给用户确认后删除（移除配置 + 清理工作区/状态目录）。
- ETA硬触发检查：读取 `memory/eta-tasks.json`，若存在到期/逾期任务，优先主动回报进度（完成或延迟+新ETA）。
- Notify user when there is meaningful progress (new merged PR, major issue update, release note mentioning these topics). If no meaningful change, stay silent.
- If actionable update is detected (e.g., available upgrade, required migration, important fix), keep reminding user on subsequent heartbeats until user explicitly confirms handled/ignored.
