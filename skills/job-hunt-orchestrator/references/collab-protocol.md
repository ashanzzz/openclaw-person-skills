# Zero ↔ Coder 协作协议

## 角色
- Zero（CEO）：目标拆解、验收定义、质量门控、对用户汇报
- Coder（执行）：脚本开发、抓取执行、结果打包

## 通讯对象

### 1) 任务单
- task_id
- target_region
- constraints
- expected_fields
- deadline

### 2) 结果包
- raw_records.json
- normalized_records.json
- error_log.txt
- coverage_report.md

### 3) 质检单（Zero出）
- pass/fail
- failed_rules
- rework_items

### 4) 返工单
- round(1/2/3)
- exact gaps
- required fixes

## 终止条件
- 通过质检：交付用户
- 连续3轮失败：向用户汇报阻塞点与替代方案
