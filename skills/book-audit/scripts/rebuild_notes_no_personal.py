#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
重建9本书的切片笔记（中立版，无个人内容），并生成统一审核报告与强化版 master.md。
"""
import os
import re
import json
import html
from collections import Counter

BASE = "/root/.openclaw/workspace/kb/books-notes"
BOOKS = [
    "驱动力",
    "人性的弱点",
    "格鲁夫给经理人的第一课",
    "第五项修炼",
    "管理的常识",
    "精益思想",
    "领导梯队",
    "丰田模式",
    "高效能人士的七个习惯",
]

AD_PATTERNS = ["读累了记得休息", "公众号", "沉金书屋", "电子书搜索下载"]
STOPWORDS = set([
    "我们", "他们", "这个", "那个", "以及", "一个", "一种", "如何", "什么", "通过", "进行", "没有", "可以", "需要", "就是",
    "组织", "管理", "学习", "公司", "工作", "系统", "问题", "能力", "阶段", "章节", "内容", "作者", "模型", "方法",
])

MASTER_TEMPLATES = {
    "驱动力": {
        "one_liner": "高绩效来自内在动机：自主、专精、目的，比外在奖惩更可持续。",
        "framework": ["驱动力1.0（生存本能）", "驱动力2.0（奖惩机制）", "驱动力3.0（内在动机）", "三要素：自主、专精、目的"],
        "sop": ["识别任务类型：机械型/创造型", "机械型任务可用清晰奖惩", "创造型任务优先提升自主权", "建立持续反馈机制支持专精提升", "将任务与更大目的连接"],
        "pitfalls": ["把所有任务都当成可用奖金驱动", "只追求短期产出忽视长期学习", "忽略公平导致激励失效"],
    },
    "人性的弱点": {
        "one_liner": "高质量人际关系建立在尊重、倾听与真诚赞赏，而非指责与对抗。",
        "framework": ["不批评、不责备、不抱怨", "真诚赞赏", "唤起他人内在意愿", "站在他人视角思考"],
        "sop": ["先听后说，先复述对方关切", "表达具体而真诚的认可", "提出建议时先讲共同目标", "保留对方面子与选择权", "用事实与行动建立信任"],
        "pitfalls": ["用道理压人", "把反馈变成否定人格", "把沟通目标设为“赢辩论”而非“达成共识”"],
    },
    "格鲁夫给经理人的第一课": {
        "one_liner": "经理人的产出来自“影响力杠杆”，核心是通过系统与他人放大组织绩效。",
        "framework": ["经理人产出公式", "管理杠杆率", "会议系统设计", "决策流程与执行闭环", "人才管理（招、评、育、留）"],
        "sop": ["定义团队产出指标", "把时间投入高杠杆活动（1:1、培训、关键会议）", "用结构化会议推进信息与决策", "用评估与反馈校准绩效", "持续建设人才梯队"],
        "pitfalls": ["事必躬亲导致低杠杆", "会议无议程无结论", "只看结果不建设能力系统"],
    },
    "第五项修炼": {
        "one_liner": "组织学习的核心在于系统思考：看结构、看反馈、看长期，而非只追逐事件。",
        "framework": ["五项修炼：系统思考、自我超越、心智模式、共同愿景、团队学习", "系统基本模式", "杠杆点思维"],
        "sop": ["先界定问题边界与关键变量", "绘制因果回路识别反馈", "定位高杠杆干预点", "通过团队汇谈校准心智模式", "以小范围原型验证并迭代扩展"],
        "pitfalls": ["只救火不改结构", "把短期症状当根因", "缺乏反思机制导致同类问题反复"],
    },
    "管理的常识": {
        "one_liner": "管理是把复杂现实转化为可执行系统：目标清晰、责任明确、反馈及时。",
        "framework": ["目标管理", "组织协同", "执行与复盘", "变革适应"],
        "sop": ["明确业务目标与衡量标准", "拆分责任到岗位与时间节点", "建立例会与复盘节奏", "识别外部变化并快速调整", "把经验沉淀为流程"],
        "pitfalls": ["目标模糊", "职责重叠无人负责", "只布置不复盘"],
    },
    "精益思想": {
        "one_liner": "精益的本质是持续消除浪费，让价值稳定、顺畅、可持续地流向客户。",
        "framework": ["五原则：定义价值、识别价值流、流动、拉动、尽善尽美", "七种浪费"],
        "sop": ["从客户价值重新定义流程", "梳理价值流并标记浪费点", "重排流程减少等待与搬运", "建立拉动机制降低库存", "持续改善形成标准作业"],
        "pitfalls": ["把精益当成本削减口号", "只做局部优化不看端到端", "改善无数据验证"],
    },
    "领导梯队": {
        "one_liner": "领导力不是一次性晋升，而是六个阶段的连续角色转变与能力迁移。",
        "framework": ["六阶段转变", "三维度：领导技能、时间管理、工作理念", "继任与梯队建设"],
        "sop": ["识别当前层级与下一层级要求", "评估技能/时间/理念差距", "制定阶段化发展计划", "通过教练与轮岗加速转变", "建立继任与评估机制"],
        "pitfalls": ["升职不转型", "用旧层级习惯做新层级工作", "忽视继任导致断层"],
    },
    "丰田模式": {
        "one_liner": "丰田模式以长期主义、现场主义与持续改善构建高质量、低浪费的运营系统。",
        "framework": ["14项原则", "长期主义", "现场现物（Gemba）", "尊重人并培养人", "持续改善（Kaizen）"],
        "sop": ["以长期价值定义经营目标", "到现场观察并基于事实决策", "标准化作业并暴露异常", "用问题解决循环持续改善", "建设人才与文化双轮驱动"],
        "pitfalls": ["只学工具不学原则", "数据脱离现场", "短期KPI挤压长期能力建设"],
    },
    "高效能人士的七个习惯": {
        "one_liner": "高效能建立在原则导向的习惯系统：先修炼自我，再实现协同，最后持续更新。",
        "framework": ["个人成功：积极主动、以终为始、要事第一", "公众成功：双赢思维、知彼解己、统合综效", "持续更新：不断更新"],
        "sop": ["每周明确角色与关键目标", "按重要不紧急优先安排时间", "沟通前先理解对方", "在冲突中寻找双赢方案", "固定节奏做身心智灵更新"],
        "pitfalls": ["目标与日程脱节", "只追求效率不追求原则", "忽视长期更新导致透支"],
    },
}


def read_text(path: str) -> str:
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


def clean_slice_text(raw: str) -> str:
    lines = raw.splitlines()
    # slice 文件一般前几行是元信息
    body = "\n".join(lines[4:]) if len(lines) > 4 else raw
    body = html.unescape(body)
    body = body.replace("\u00a0", " ").replace("&#13;", "\n")
    body = re.sub(r"\s+", " ", body).strip()
    return body


def classify_page(text: str) -> str:
    if not text:
        return "空白页"
    if any(p in text for p in AD_PATTERNS):
        return "广告/噪声页"
    if "图书在版编目" in text or "CIP" in text or "Copyright" in text or "ISBN" in text:
        return "版权/出版信息页"
    if re.search(r"\b目录\b|\bContents\b", text):
        return "目录页"
    if "致谢" in text:
        return "致谢页"
    if "附录" in text:
        return "附录页"
    if re.search(r"第[一二三四五六七八九十0-9]+章", text) or re.search(r"\|第\d+章\|", text):
        return "章节正文"
    return "正文/其他"


def extract_topic(text: str, page_type: str) -> str:
    if page_type in ["广告/噪声页", "空白页"]:
        return "非正文内容"
    m = re.search(r"(第[一二三四五六七八九十0-9]+章[^。！？\n]{0,40})", text)
    if m:
        return m.group(1).strip()
    m2 = re.search(r"(\|第\d+章\|[^。！？\n]{0,40})", text)
    if m2:
        return m2.group(1).strip()
    # fallback: 取前 28 字
    t = text[:28].strip()
    return t if t else "本页主题"


def split_sentences(text: str):
    sents = re.split(r"[。！？；!?;]", text)
    out = []
    for s in sents:
        s = re.sub(r"\s+", " ", s).strip()
        if len(s) < 12:
            continue
        if any(p in s for p in AD_PATTERNS):
            continue
        out.append(s)
    return out


def extract_bullets(text: str, page_type: str):
    if page_type == "广告/噪声页":
        return ["该页主要为来源广告或引流信息，不构成书籍正文知识点。"]
    if page_type == "空白页":
        return ["该页无可提炼的正文内容。"]

    sents = split_sentences(text)
    if not sents:
        return ["该页以元数据或结构信息为主，正文信息有限。"]

    bullets = []
    for s in sents[:4]:
        # 压缩过长句
        if len(s) > 110:
            s = s[:110] + "…"
        bullets.append(s)
    return bullets[:3]


def extract_keywords(text: str, page_type: str):
    if page_type in ["广告/噪声页", "空白页"]:
        return ["噪声页"]

    # 提取 2~6 字中文短词
    words = re.findall(r"[\u4e00-\u9fa5]{2,6}", text)
    words = [w for w in words if w not in STOPWORDS and len(w) >= 2]
    if not words:
        return ["概要"]
    c = Counter(words)
    keys = [w for w, _ in c.most_common(12)]

    # 去重（前缀重合过滤）
    final = []
    for k in keys:
        if any(k in x or x in k for x in final):
            continue
        final.append(k)
        if len(final) >= 5:
            break
    return final if final else ["概要"]


def build_note(book: str, slice_num: str, text: str) -> str:
    page_type = classify_page(text)
    topic = extract_topic(text, page_type)
    bullets = extract_bullets(text, page_type)
    keywords = extract_keywords(text, page_type)

    lines = []
    lines.append(f"# {book} — Slice {slice_num} 笔记")
    lines.append("")
    lines.append("## 页面类型")
    lines.append(f"- {page_type}")
    lines.append("")
    lines.append("## 主题")
    lines.append(f"- {topic}")
    lines.append("")
    lines.append("## 摘要")
    for b in bullets:
        lines.append(f"- {b}")
    lines.append("")
    lines.append("## 关键词")
    for k in keywords:
        lines.append(f"- {k}")
    lines.append("")
    return "\n".join(lines)


def chapter_map_from_slices(book_dir: str):
    slices = sorted([f for f in os.listdir(book_dir) if re.match(r"^slice_\d+\.md$", f)], key=lambda x: int(re.findall(r"\d+", x)[0]))
    mapping = []
    for f in slices:
        p = os.path.join(book_dir, f)
        txt = clean_slice_text(read_text(p))
        m = re.search(r"(第[一二三四五六七八九十0-9]+章[^。！？\n]{0,50})", txt)
        if not m:
            m = re.search(r"(\|第\d+章\|[^。！？\n]{0,50})", txt)
        if m:
            title = re.sub(r"\s+", " ", m.group(1)).strip()
            mapping.append((f, title))
    # 去重保序
    seen = set()
    out = []
    for f, t in mapping:
        key = t
        if key in seen:
            continue
        seen.add(key)
        out.append((f, t))
    return out[:18]


def build_master(book: str, book_dir: str) -> str:
    tpl = MASTER_TEMPLATES[book]
    chapter_map = chapter_map_from_slices(book_dir)

    lines = []
    lines.append(f"# {book} — 强化版 Master 笔记")
    lines.append("")
    lines.append("## 一句话总纲")
    lines.append(f"- {tpl['one_liner']}")
    lines.append("")
    lines.append("## 核心框架")
    for x in tpl["framework"]:
        lines.append(f"- {x}")
    lines.append("")
    lines.append("## 章节地图（按切片抽取）")
    if chapter_map:
        for f, t in chapter_map:
            lines.append(f"- {f}: {t}")
    else:
        lines.append("- 本书章节标题在切片中未完整抽取，已以核心框架替代。")
    lines.append("")
    lines.append("## 可复用执行 SOP")
    for i, s in enumerate(tpl["sop"], 1):
        lines.append(f"{i}. {s}")
    lines.append("")
    lines.append("## 常见误区")
    for p in tpl["pitfalls"]:
        lines.append(f"- {p}")
    lines.append("")
    lines.append("## 使用方式")
    lines.append("- 先阅读本文件建立全局模型，再按需要下钻到对应 slice_XXX_n.md。")
    lines.append("- 将书中框架映射到真实场景时，优先做小规模试点，再标准化推广。")
    lines.append("")
    return "\n".join(lines)


def update_meta(book_dir: str, total_slices: int):
    meta_path = os.path.join(book_dir, "meta.json")
    meta = {}
    if os.path.exists(meta_path):
        try:
            meta = json.loads(read_text(meta_path))
        except Exception:
            meta = {}
    meta.setdefault("notes_style", "neutral-slice-notes-v2")
    meta["status"] = "completed"
    meta["slice_total"] = total_slices
    meta["note_total"] = total_slices
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)


def run():
    audit_rows = []
    total_new = 0
    total_books = 0

    for book in BOOKS:
        book_dir = os.path.join(BASE, book)
        if not os.path.isdir(book_dir):
            audit_rows.append((book, 0, 0, 0, "目录缺失"))
            continue

        total_books += 1
        slice_files = sorted([f for f in os.listdir(book_dir) if re.match(r"^slice_\d+\.md$", f)], key=lambda x: int(re.findall(r"\d+", x)[0]))

        if not slice_files:
            audit_rows.append((book, 0, 0, 0, "无切片"))
            continue

        generated = 0
        for sf in slice_files:
            num = re.findall(r"\d+", sf)[0]
            slice_path = os.path.join(book_dir, sf)
            txt = clean_slice_text(read_text(slice_path))
            note = build_note(book, num, txt)
            note_path = os.path.join(book_dir, f"slice_{num}_n.md")
            with open(note_path, "w", encoding="utf-8") as f:
                f.write(note)
            generated += 1

        # 重建 master
        master = build_master(book, book_dir)
        with open(os.path.join(book_dir, "master.md"), "w", encoding="utf-8") as f:
            f.write(master)

        # 更新 meta
        update_meta(book_dir, len(slice_files))

        total_new += generated
        audit_rows.append((book, len(slice_files), generated, 0, "完成"))

    # 审核报告
    report_path = os.path.join(BASE, "QA-九本书复核报告.md")
    lines = []
    lines.append("# 九本书复核报告（切片与笔记）")
    lines.append("")
    lines.append("- 目标：逐书审核切片与笔记一致性，重建中立笔记（不含个人内容），并输出强化版 master。")
    lines.append("- 范围：9 本书。")
    lines.append("")
    lines.append("## 结果总览")
    lines.append("")
    lines.append("| 书名 | 切片数 | 笔记重建数 | 缺失 | 状态 |")
    lines.append("|---|---:|---:|---:|---|")
    for b, t, g, m, s in audit_rows:
        lines.append(f"| {b} | {t} | {g} | {m} | {s} |")
    lines.append("")
    lines.append(f"- 完成书籍：{total_books} 本")
    lines.append(f"- 切片笔记重建总数：{total_new} 篇")
    lines.append("- 备注：切片正文保留在本地用于审阅；对外提交仅包含笔记与技能。")

    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"DONE books={total_books} notes={total_new} report={report_path}")


if __name__ == "__main__":
    run()
