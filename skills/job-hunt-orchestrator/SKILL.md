---
name: job-hunt-orchestrator
description: 全链路岗位检索与质检编排。用于用户要求“找工作/找岗位/官网招聘/区域内岗位/发布时间/薪资/岗位要求/投递链接”时。执行官网优先+浏览器详情核验+结构化评分+异常兜底，输出可直接投递清单。
---

# Job Hunt Orchestrator

执行目标：给出“可投递成品”，不是信息碎片。

## 输入参数（必须先确认）
- 区域：城市/区县/半径（如 `天津东丽/滨海/空港 30km`）
- 方向：行业/岗位关键词（如 `制造运营/质量/供应链/商业分析`）
- 层级：实习/社招/资深
- 偏好：外企优先、劳动法友好（五险一金/工时/加班补偿/假期）
- 公司池（可选）：用户指定公司名单；若为空则自动扩展发现

## 数据源优先级（严格）
1. 企业官网招聘页（最高）
2. 官方 ATS（Workday/SuccessFactors/Oracle Taleo 等）
3. 一线招聘站（LinkedIn/智联/BOSS）
4. 聚合站（仅补充线索，不直接作为最终证据）

详见：`references/source-priority.md`

## 执行链路（标准流水线）
1. 建企业池（区域内目标企业名单）
2. 并行执行两条方案：
   - 方案A（定向）：按用户提供公司池逐家检索官网/ATS
   - 方案B（扩展）：在区域内持续发现新增优质公司并检索岗位
3. 使用浏览器点进岗位详情页核验字段
4. 抽取统一字段并去重
5. 评分与分桶（立即投递/可观察/待核验）
6. 覆盖率核对（公司覆盖、岗位覆盖、失败重试）
7. 质量门控，不达标返工

## 输出字段合同（硬约束）
每个岗位必须包含（缺一则不达标）：
- `company`
- `position_title`
- `location`
- `distance_km`
- `posted_date`
- `salary`
- `requirements_summary`
- `official_job_url`（必填）
- `apply_url`（必填）
- `laborlaw_signals`
- `labor_law_score`（high/medium/low）
- `fit_score`（0-100）
- `bucket`（apply_now/watchlist/verify_needed）

详见：`references/output-contract.md`

## 质量门控（CEO规则）
- 未点进详情页：禁止交付
- 无 `official_job_url` 或 `apply_url`：禁止进入推荐清单
- 无发布日期：仅可进入 `verify_needed`
- 聚合站且无官网回链：降级并标注风险
- 最多返工 3 轮，超限时上报阻塞与替代方案

## 异常处理（必须执行）
- 浏览器不可用：切换静态抓取 + 标 `verify_needed`
- 页面反爬/登录墙：请求人工一步登录后继续
- 字段抽取失败：保留原文片段并重试抽取

详见：`references/exception-playbook.md`

## 协作协议（Zero ↔ 代码专家）
- Zero 负责：目标拆解、门控、最终交付
- 代码专家负责：抓取脚本、解析脚本、批处理运行
- 通讯格式：`任务单 -> 结果包 -> 质检单 -> 返工单`

详见：`references/collab-protocol.md`

## 本地脚本
- `scripts/normalize_jobs.py`：字段标准化 + 去重
- `scripts/score_jobs.py`：岗位评分与分桶
