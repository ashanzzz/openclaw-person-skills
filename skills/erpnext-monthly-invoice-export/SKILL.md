---
name: erpnext-monthly-invoice-export
version: 2.0.0
description: |
  Install: clawhub install erpnext-monthly-invoice-export

  Export/download ERPNext invoices for a given company + month (e.g., {{公司简称A}} 2026年1月), including unpaid. Uses ERPNext REST API token from secure/api-fillin.env, saves CSV/JSON/summary under secure/erpnext/exports/. Also serves as the master reference for 阿山's ERPNext operational habits.
---

# ERPNext 全操作规范（阿山专用）

## 账户与权限（重要）

- **单一账户同时拥有{{公司简称A}}和{{公司简称B}}两家公司权限**，无需分开认证
- 查/创建单据时用 `company` 字段区分公司
- 公司精确名称（从 ERPNext UI 复制）：
  - {{公司简称A}}：`{{公司名}}`
  - {{公司简称B}}：`{{公司名}}`

## API 基础

- Base URL：`http://192.168.8.11:8888`（来自 `ERP_BASE_URL`）
- 认证：`Authorization: Token <api_key>:<api_secret>`（来自 `ERP_API_TOKEN`）
- 单一真源：`/root/.openclaw/workspace/secure/api-fillin.env`
- **禁止在聊天中回显 token**

## API 操作规范

| 操作 | 方法 | 端点 | 说明 |
|------|------|------|------|
| 查单据 | GET | `/api/resource/<Doctype>/<name>` | |
| 更新草稿 | PUT | `/api/resource/<Doctype>/<name>` | 必须带全必填字段 |
| 提交单据 | POST | `/api/resource/<Doctype>/<name>` | docstatus=1 |
| 撤销提交 | POST | `/api/resource/<Doctype>/<name>` | docstatus=0 |
| 删草稿 | DELETE | `/api/resource/<Doctype>/<name>` | |

**注意**：POST 到单个单据用于更新草稿；PUT 用于完整替换。

## ERPNext 操作习惯（阿山专用）

### Payment Entry（付款凭证）操作规范

**创建或更新草稿时，mode_of_payment 必须明确**。
- 如果用户**没有明确指定**付款方式，必须先**询问用户**：`电汇 / 现金 / 支票 / 信用卡 / 银行汇票`？
- 切忌在用户未确认的情况下自行填写默认值。

更新时必须同时传入以下字段，否则报 ValidationError：
- `posting_date` — 业务日期
- `reference_date` — 银行交易日期
- `reference_no` — 银行流水号（无则填"自动调整"）
- `mode_of_payment` — 付款方式（{{公司简称A}}常用：`电汇`）

其他可查的 mode_of_payment：`支票`、`信用卡`、`银行汇票`、`现金`、`电汇`

```bash
# 正确示范
curl -X PUT "${ERP_BASE_URL}/api/resource/Payment%20Entry/ACC-PAY-2026-00132" \
  -H "Authorization: Token $ERP_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "posting_date": "2026-02-28",
    "reference_date": "2026-02-28",
    "reference_no": "自动调整",
    "mode_of_payment": "电汇"
  }'
```

### Purchase Invoice（采购发票）操作规范

**创建时**：
- `posting_date`：过账日期，设置 `set_posting_time=1` 可保留用户指定日期
- `company`：精确公司名称
- `supplier`：供应商名称
- `items[].item_code`：物料代码
- `items[].qty`：数量
- `items[].rate`：单价
- `items[].custom_guige_xinghao`：规格型号（主匹配字段，**弃用 description**）

**提交后发现 posting_date 错误**：
取消提交 → 删除 → 重建，并设置 `set_posting_time=1`

**匹配规则**：
- 优先用 `item_name` + `custom_guige_xinghao` 匹配
- **弃用 description** 作为主判断依据
- 物料名写通用名（不含营销词/品牌词/包装宣传语）
- 规格型号只保留核心识别信息
- 不写"几支装/几盒装"等包装数量（除非识别或计价必需）

示例：
- `水性笔 | 0.5mm 黑色` ✓
- `硒鼓 | 三星 SCX-4521HS` ✓

### Material Request（物料申请）操作规范

- 创建后需提交（submit）才生效
- `material_request_type`：采购/转移/制造

### 常用单据类型前缀

- 付款：`ACC-PAY-.YYYY.-`
- 采购发票：`ACC-PINV-.YYYY.-`
- 销售发票：`ACC-SINV-.YYYY.-`
- 物料申请：`MAT-REQ-.YYYY.-`

## 日期处理规范

- ERPNext 默认 posting_date 会自动设为当天
- 需要录入历史日期时：创建时设置 `set_posting_time=1`，然后传 `posting_date`
- 草稿阶段可以直接修改 posting_date；提交后需要先取消再重建

## 查询语法

```bash
# 查某公司某月所有采购发票
GET /api/resource/Purchase%20Invoice?filters=[["company","=","{{公司名}}"],["posting_date","between",["2026-02-01","2026-02-28"]]]

# 查草稿状态单据
GET /api/resource/Purchase%20Invoice?filters=[["docstatus","=",0]]
```

## 额度/限制

- ERPNext API 无每日额度限制
- 但频繁大量查询建议加 `limit=100` 等分页参数

---

# 月度发票导出（子模块）

## When to use
- 用户说：下载/导出 ERPNext 某公司（如"{{公司简称A}}"）某个月（如 2026-01）的**发票/单据**，**未付款也要**，并要求"记录好、保存好、可复用"。

默认口径：**Purchase Invoice（采购发票）**；如用户要销售发票则改为 **Sales Invoice**。

## Inputs (ask if missing)
- `company`：ERPNext 里的公司名称
- `month`：`YYYY-MM`（例如：`2026-01`）
- `doctype`：`Purchase Invoice` 或 `Sales Invoice`
- 是否需要逐张 PDF（默认：否，只导出清单 CSV + 汇总）

## Quick run
```bash
python3 skills/erpnext-monthly-invoice-export/scripts/export_erpnext_invoices.py \
  --month 2026-01 \
  --company "{{公司简称A}}" \
  --doctype "Purchase Invoice"
```

## Outputs
输出目录（自动创建）：
- `secure/erpnext/exports/<company>/<month>/`
  - `invoices_<doctype>_<month>.csv`
  - `invoices_<doctype>_<month>.json`
  - `summary_<doctype>_<month>.md`
  - `no_invoice_<doctype>_<month>.csv`（无票支出：bill_no 为空/0/全0）

## 发票台账输出格式（调用 purchase-invoice-classifier）

完成 export 后，调用 `purchase-invoice-classifier` skill 做四级分类输出：

**分类（四级）**：电汇 / 现金 / 无发票 / 未付款
**格式**：每行一个物料明细（不是按发票汇总）
**字段**：凭证号 / 发票号码 / 日期 / 供应商 / 物料名称 / 规格型号 / 备注 / 数量 / 金额

详见 `skills/purchase-invoice-classifier/SKILL.md`

## Troubleshooting
- HTTP 401：token 失效 → 重新生成并更新 `ERP_API_TOKEN`
- 公司名不匹配：从 ERPNext UI 复制精确值
