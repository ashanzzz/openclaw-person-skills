---
name: erpnext-account-report
description: |
  ERPNext 账单导出 + 付款勾稽 + 明细分拆。导出指定公司+指定账户+日期范围的完整收支明细（物料级），并与付款凭证、采购发票自动勾稽。
  触发词：导出账单 / 导出账户明细 / 生成账单报告 / 导出银行流水 / 导出现金流水 /
          账单匹配付款 / 导出 erpnext 账单
---

# ERPNext 账单导出 → 付款勾稽 → 明细分拆

## 何时使用

用户说「导出账单/账户明细/账单报告」且指定公司+账户+月份时使用。

## 输入参数

| 参数 | 说明 | 示例 |
|------|------|------|
| `--company` | 公司完整名称 | `天津祺富机械加工有限公司` |
| `--account` | 账户完整名称（含-公司后缀） | `现金账单-孟祥山 - 祺富` |
| `--from` | 起始日期 | `2026-01-01` |
| `--to` | 截止日期 | `2026-01-31` |
| `--output` | 输出 xlsx 路径 | `/path/to/output.xlsx` |

常用账户：
- 祺富现金：`现金账单-孟祥山 - 祺富`
- 祺富银行：`银行账单 - 祺富`
- 吉众现金/银行：查 Account 列表确认

## 输出字段

每行 = 1个物料明细（1个付款凭证 → 1个发票凭证 → 1个物料）

| 字段 | 说明 |
|------|------|
| 凭证号 | Payment Entry 或 Purchase Invoice 编号 |
| 凭证日期 | GL 过账日期 |
| 类型 | `Payment Entry` / `Purchase Invoice` / 其他 |
| 供应商/对方 | 供应商名称（against 字段） |
| 付款方式 | 现金/电汇/支票（来自 PE 的 mode_of_payment） |
| 项目名(物料名) | 物料名称 item_name |
| 规格型号 | custom_guige_xinghao |
| 单价 | rate（含税单价） |
| 数量 | qty |
| 单位 | uom |
| 发票号码 | bill_no（来自 Payment Entry Reference） |
| 分配金额 | 按比例分配的付款金额（支出=credit，收入=debit） |
| 借贷方向 | 支出（credit）/ 收入（debit） |
| 备注 | custom_备注 |

## 数据链路

```
GL Entry（账户+日期筛选）
│
├── voucher_type = Payment Entry
│   └── Payment Entry
│       └── references (Payment Entry Reference)
│           ├── reference_doctype = Purchase Invoice
│           └── reference_name → Purchase Invoice
│               └── items (Purchase Invoice Item) × N
│                   → 每 item 1 行，分配金额按 PI 总额比例分摊
│
└── voucher_type = Purchase Invoice（直接 PI，如房租/电费）
    └── Purchase Invoice
        └── items × N
```

## 执行命令

```bash
cd skills/erpnext-account-report/scripts
python3 generate.py \
  --company "{{公司名称}}" \
  --account "{{账户名称}}" \
  --from "{{起始日期}}" \
  --to "{{截止日期}}" \
  --output "{{输出路径}}"
```

## 质量检查

- [ ] 总行数 ≥ GL Entry 条数（因为多物料PI会拆成多行）
- [ ] 支出合计 ≈ 账户 GL 的 credit 总和
- [ ] 每行分配金额 > 0
- [ ] 借贷方向与金额正负一致（支出=正数，收入=正数）
- [ ] 如有差异金额 > 1元，检查是否 PI 分摊尾差

## 注意事项

- Payment Entry 的 `paid_amount` = GL 的 credit，方向为「支出」
- 1个 PE 关联多个 PI → 每个 PI 分别展开
- 1个 PI 包含多个物料 → 每行一个物料，金额按比例分配
- 发票号码 `bill_no` 来自 Payment Entry Reference，而非 PI 本身
- `custom_guige_xinghao` = 规格型号（主匹配字段，不是 description）

## 依赖

- Python 3.12+
- `openpyxl`（虚拟环境：`~/.openclaw/workspace/.venv-xls`）
- ERPNext API token（从 `secure/api-fillin.env` 读取 `ERP_API_TOKEN`）
- ERPNext Base URL（`ERP_BASE_URL`，默认 `http://192.168.8.11:8888`）
