# Career DB 使用说明

数据库文件：`secure/career-db/career_jobs.sqlite`

## 核心表
- `companies`：公司主数据
- `jobs`：岗位数据（与公司关联）
- `search_runs`：每次检索批次日志

## 强制执行规则
1. 每次检索前先读：
   - `profile_user.md`
   - `profile_girlfriend.md`
2. 每次检索后必须回写：
   - 新增/更新公司到 `companies`
   - 新增/更新岗位到 `jobs`
   - 批次统计到 `search_runs`
3. 对女朋友岗位，必须填写：
   - `fit_for_girlfriend`（0/1）
   - `fit_reason`
4. 不适配岗位可存档，但对外输出时必须PASS（不推荐）

## 快速查询示例
```sql
-- 查看适配女朋友的岗位
SELECT c.name, j.title, j.location, j.posted_date, j.official_job_url
FROM jobs j
JOIN companies c ON c.id = j.company_id
WHERE j.fit_for_girlfriend = 1
ORDER BY j.posted_date DESC;

-- 查看最近检索批次
SELECT * FROM search_runs ORDER BY id DESC LIMIT 20;
```
