# WORKFLOW_AUTO.md

本文件用于在上下文压缩/重启后快速恢复 Zero 的工作协议（自动化工作流提示）。

## 启动顺序（主会话）
1. 读取：SOUL.md、USER.md、AGENTS.md
2. 读取：memory/今天.md（必要时昨天）
3. 需要回忆“过去做过什么/决定/偏好/待办”时：先 memory_search，再 memory_get

## 官方学习门控（高优先级）
- 涉及 OpenClaw 配置/行为/更新：先核验官方来源（本地 /app/docs + 在线 docs.openclaw.ai），再改。
- 改完必须：openclaw doctor + openclaw status --all。

## 多任务并行（单一 agent 也适用）
- 耗时动作优先放后台（exec background / 任务会话），并显式维护：job_id、ETA、下一次回报点。

## 多 agent（如未来恢复）
- 默认按异步投递+回收：sessions_send(timeoutSeconds=0) + sessions_history 回收。
- 强制状态协议：ACK/PROGRESS/DONE/FAIL + job_id；超时≠失败，必须二次核验。
- 往返门控：单 job 的 Zero↔Agent 往返软上限 **≤20**；能提前 DONE 就提前。
- 交互压缩模板（默认用一次性澄清清单，避免碎片问答）：
  - Agent 首轮必须输出：`ACK + 关键澄清问题清单(<=N条) + 可执行方案A/B + DONE判定条件`
  - Zero 只补最小必要信息；满足 DONE 条件立即回 `DONE(job_id=...)` 并停止该 job。

## 对外输出
- 避免空话，直接给结论+下一步。
- 用户要求“附件”时：通过聊天渠道直接发送文件（message 工具），不要只给路径。
