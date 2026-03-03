# 职业发展专家/HR 强制检索源

每次岗位检索前，必须先读取以下文件：

1. `secure/career-db/profile_user.md`
2. `secure/career-db/profile_girlfriend.md`
3. `secure/career-db/career_jobs.sqlite`（companies/jobs表）
4. `secure/career-db/README.md`

## 强制规则
- 未读取上述文件，不得输出岗位结论。
- 先查历史公司与岗位，避免重复和遗漏。
- 结果必须回写数据库（公司、岗位、链接、发布时间、适配结论）。
