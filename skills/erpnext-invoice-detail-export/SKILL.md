# SKILL.md — ERPNext 发票明细导出

将 ERPNext Purchase Invoice 按月导出为标准化 Excel 发票明细表。

## 核心格式规范

**Excel 列结构（8列，无合计列）：**

| 列号 | 字段 | 说明 |
|------|------|------|
| A | 序号 | 数字，从1开始 |
| B | 发票号码 | `bill_no`，文本格式（@），勿用 PI name |
| C | 发票日期 | Excel 日期序列数，格式 `yyyy"年"mm"月"dd"日"`（如 2026年03月31日）|
| D | 发票类型 | 普通发票 / 专用发票 / 定额发票（由税率推断） |
| E | 发票项目 | 原始 `item_name` 经「名称风格规范化」后写入 |
| F | 金额 | **含税合计金额**（勿填单独税额） |
| G | 购买方式 | 根据 expense_account 推断：含"暂估/库存"→购买申请，含"管理"→报销申请，其余→费用 |
| H | 支付方式 | 固定写"现金" |

**格式规范：**
- 字体：等线
- 标题行（第1行）：size=12，加粗，居中，行高28，合并A1:H1
- 列标题行（第2行）：size=10，行高20
- 数据行：size=9，行高16.5
- 边框：全边框 thin，颜色 #000000
- 对齐：全部居中
- 列宽（参考）：A=4.5, B=16, C=13, D=7, E=18, F=11, G=8, H=7

**日期序列转换（Python）：**
```python
from datetime import datetime
serial = (datetime.strptime("2026-03-31", "%Y-%m-%d") - datetime(1899, 12, 30)).days
# 结果：45397
# Excel 格式：'yyyy"年"mm"月"dd"日"'
```

## 发票项目名称风格判断原则（重要！核心逻辑）

> 来自阿山的实际风格，固化为本 skill 的判断原则。

**背景：** 当前输出的是「发票」而非「发票明细」，即只写发票上的品目名称。但 ERPNext 里同品目可能跨月出现（如3月电费、4月电费），Excel 需要能区分不同月份。

### 分类原则

| 类别 | 特征 | 处理方式 |
|------|------|---------|
| **总结类** | 品目本身是泛称，月度间无天然区分度（如"电费"每月都有） | **智能加时间戳**：`{yyyy}年{mm}月` + 原品目 |
| **明细类** | 品目本身已够具体，不同供应商/月度的同名品目无需再区分 | **保持原样** |

### 总结类关键词（需加时间前缀）

| 关键词 | 转换示例 |
|--------|---------|
| 电费 | `2026年03月电费` |
| 水冰雪、自来水、水费 | `2026年03月水费` |
| 车用油、汽油、柴油、机油 | `2026年03月车用油` |

### 明细类（不改）

`轿车保险`、`咨询服务费`、`员工餐费`、`快递费`、具体品目（门扣/通止规/水性笔等）

### 判断方法（智能判断，不是固定匹配）

1. 看品目是否"月度间天然可区分"：同一供应商每月都有"电费"→需要加时间区分；"咨询服务费"各月内容不同→不需要
2. 看品目是否过于泛称："电费"本身看不出哪个月→加时间；"员工餐费"已足够具体→不加
3. **不确定时保守处理**：宁可保留原名，也不随意加时间戳

### 注意事项

- **脚本不做这个判断**，由 Agent 读取 PI 数据后根据 `posting_date` 智能决定
- **不要把脚本写成固定关键词替换**，这是原则性判断，需要 Agent 理解品目语义
- 如遇到新的总结类品目（如"燃气费""蒸汽费"），参照同样逻辑处理

### 判断逻辑
1. 取 PI 的 `posting_date`（格式 `YYYY-MM-DD`）
2. 提取 yyyy 和 mm
3. 按关键词匹配，应用上述规则
4. 未匹配到的品目保留原始 `item_name`

## 发票类型判断（优先 custom_发票类型）

**优先规则：**
1. 读取 PI 的 `custom_发票类型` 字段（ERPNext 自定义字段）
2. 若为空，用税率推断：
   - `rate == 0` → 定额发票
   - `abs(rate - 13) < 0.01` → 专用发票
   - 其他税率 → 普通发票

## 使用方式

### 步骤1：从 ERPNext 导出当月 PI 列表

```python
# 查询公司某月所有已提交 Purchase Invoice
filters = [
    ["company", "=", "{{公司名}}"],
    ["posting_date", "between", ["2026-03-01", "2026-03-31"]]
]
fields = ["name","posting_date","supplier","supplier_name","bill_no","bill_date","grand_total","outstanding_amount","docstatus"]
```

### 步骤2：查询每个 PI 的行项目和税额

```python
# 对每个 PI name 调用（curl）：
curl -s "http://192.168.8.11:8888/api/resource/Purchase%20Invoice/{pi_name}?fields=%5B%22items%22%2C%22taxes%22%2C%22custom_%E5%8F%91%E7%A5%A8%E7%B1%BB%E5%9E%8B%22%5D" \
  -H "Authorization: Token {ERP_KEY}:{ERP_SECRET}"
```

### 步骤3：展开行项目并写入 Excel

**金额计算规则：**
- `gross_amount` = ERPNext 的 `amount`（含税）
- **导出金额 = gross_amount（含税合计）**

### 步骤4：发送文件

```bash
curl -s -X POST "https://api.telegram.org/bot<TOKEN>/sendDocument" \
  -F "chat_id=<CHAT_ID>" \
  -F "document=@<FILE_PATH>" \
  -F "caption=<说明文字>"
```

- Zero bot token: `8594181474:AAGqBNR9MMFINhGPhcwVRDZcAMI5Pj8M5EI`
- 阿山 chat_id: `6213495524`

## 文件路径规范

- 导出保存路径：`secure/erpnext/exports/{公司名}/{月份}/`
- 文件名格式：`{公司简称}_{月份}_发票明细.xlsx`
  - 例如：`{{公司简称B}}_2026-03_发票明细.xlsx`、`{{公司简称A}}_2026-03_发票明细.xlsx`

## 重要规则

1. **只用 `bill_no` 作为发票号码**，不能用 PI name
2. **金额 = 含税合计**，不单独列税额
3. **日期格式必须是中文** `yyyy"年"mm"月"dd"日"`
4. **发票项目名称必须经「风格规范化」处理后再写入**
5. 购买方式由 `expense_account` 字段内容推断
6. 导出前**先问用户**确认公司名和月份
7. 遇到 API 超时/错误必须排查解决，不得跳过或用已知数据凑合

## API 编码注意

ERPNext API 中 doctype 含空格（如 `Purchase Invoice`），必须用 `urllib.parse.quote` 编码。
但 Python `urllib.request.Request` 对中文 header 有 ascii 编码问题。
**推荐用 curl 发 HTTP 请求**（见步骤2示例）。

## 模板文件

参考模板：`scripts/invoice_detail_template.xlsx`

