# Output Contract (必交字段)

每条岗位输出 JSON（或表格行）需满足：

- `company`: 公司名
- `position_title`: 岗位名
- `location`: 岗位地点原文
- `distance_km`: 距离目标中心点（公里，未知则 null）
- `source_type`: official_site | official_ats | major_job_board | aggregator
- `source_url`: 来源页 URL
- `official_job_url`: 官网/官方 ATS 岗位详情 URL（必填）
- `apply_url`: 投递 URL（必填）
- `posted_date`: 发布日期（YYYY-MM-DD）
- `updated_date`: 更新日期（可空）
- `employment_type`: full_time | part_time | internship | contract | fixed_term | unknown
- `salary`: 薪资原文，无则 `未公开`
- `requirements_summary`: 要求摘要
- `responsibilities_summary`: 职责摘要
- `laborlaw_signals`: 五险一金、工时、加班、年假、合同等证据点
- `labor_law_score`: high | medium | low
- `fit_score`: 0-100
- `fit_reason`: 评分理由
- `bucket`: apply_now | watchlist | verify_needed

## 强制门槛
- `official_job_url` 缺失 => 不可进 `apply_now`
- `apply_url` 缺失 => 不可进 `apply_now`
- `posted_date` 缺失 => `bucket=verify_needed`
