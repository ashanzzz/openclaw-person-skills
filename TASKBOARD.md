# TASKBOARD

> 这是 Zero 的「任务看板」：用于把任务状态落地到可审计的文件里，方便我持续推进，也方便你随时让我导出/汇报。
>
> 你无需自己翻文件：直接在聊天里说“发我任务面板/状态”，我会把最新内容贴出来（或按你要求发附件）。

## 状态说明
- TODO：未开始
- DOING：进行中
- BLOCKED：被阻塞（通常在等你确认/等外部条件）
- DONE：完成（可验收）

## 进行中 / 阻塞中
- DOING: 让系统级“自动重试”更可靠（遇到 `Concurrency limit exceeded for account` 自动延迟 60s 后重试）
  - 现状：已通过降低并发 + 延长 timeout 降低触发概率；但尚未做到“完全自动重试原请求”。
  - 下一步：要么等待官方实现（见 openclaw/openclaw#32513），要么我写一个本地 hook/cron 机制来自动重放上一条用户请求（需要你确认可接受的行为边界）。
- DOING: 修复 web_search 工具当前不可用（ByteString/编码错误）
  - 现状：web_search 目前每次调用都会报错；临时用 gh + web_fetch 兜底。

## 待你确认（Waiting on you）
- BLOCKED: 是否需要我把 `secure/tokens/tokens.env` 作为“附件”发你（包含密钥，默认不主动外发）
- BLOCKED: `wordmonitor` 是否现在就要我安排部署试用（你希望跑在哪台机/容器？）

## 已完成（最近）
- DONE: `agents.defaults.timeoutSeconds` 提升到 1800s（缓解 long input 场景 timeout）
- DONE: `agents.defaults.maxConcurrent` 降到 1（缓解 newapi 并发/限流类报错）
- DONE: ACPX/ACP 已禁用（插件 acpx disabled；并设置 plugins.allow 白名单）
- DONE: A2A（session tools + agentToAgent）已开启可用（需要派单才会发生“互相对话”）
- DONE: MemorySearch 本地向量/FTS 可用；已对所有 agent 执行一次 index，dirty=false
- DONE: 回复署名规范：每次回复标注“由谁提供 + A2A 次数”

## 使用方式（你对我说的话术）
- “给我任务面板”（我贴 TASKBOARD 摘要）
- “给我所有 DOING/BLOCKED”（我按状态筛选）
- “job_id=XXX 现在什么情况？”（我按 job_id 汇报：状态/卡点/下一步/ETA）
- “把任务面板发成附件”（我用 Telegram 直接发文件）
