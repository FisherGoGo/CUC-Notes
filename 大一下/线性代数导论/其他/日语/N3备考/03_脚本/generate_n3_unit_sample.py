from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[3]
OUT_DIR = ROOT / "日语" / "N3备考" / "04_小单元训练"
PDF_PATH = OUT_DIR / "N3小单元训练_01_便利店与打工.pdf"
MD_PATH = OUT_DIR / "N3小单元训练_01_便利店与打工.md"


UNIT = {
    "title": "N3小单元训练 01",
    "topic": "便利店与打工",
    "goal": "练习把日常工作安排、请求、原因说明翻成自然的 N3 日语，并通过短阅读抓住原因、顺序和人物态度。",
    "focus": [
        "ておく：提前做好准备",
        "ようにする：尽量做到/养成习惯",
        "たら：如果/之后",
        "ので：客观说明原因",
        "ていただけませんか：礼貌请求",
        "わけではない：并不是...",
    ],
    "warmup": [
        ("シフト", "排班，班次", "来週のシフトを確認しました。"),
        ("レジ", "收银台", "レジでお客さんを待ちます。"),
        ("品出し", "上货，补货", "夕方は飲み物の品出しをします。"),
        ("在庫", "库存", "在庫が少ないので、店長に伝えました。"),
        ("交代する", "换班，交接", "六時に先輩と交代します。"),
        ("間に合う", "来得及", "急げば、五時のバスに間に合います。"),
    ],
    "translations": [
        {
            "cn": "因为明天早上要打工，所以我打算今晚早点睡。",
            "hint": "ので / つもり",
            "answer": "明日の朝アルバイトがあるので、今晩は早く寝るつもりです。",
        },
        {
            "cn": "请你在客人来之前，把收银台附近打扫一下。",
            "hint": "前に / てください",
            "answer": "お客さんが来る前に、レジの近くを掃除しておいてください。",
        },
        {
            "cn": "如果库存不够，请马上告诉店长。",
            "hint": "たら / てください",
            "answer": "在庫が足りなかったら、すぐ店長に伝えてください。",
        },
        {
            "cn": "我尽量在上班前确认当天的排班。",
            "hint": "ようにする / 前に",
            "answer": "仕事に入る前に、その日のシフトを確認するようにしています。",
        },
        {
            "cn": "我不是不想帮忙，只是今天身体不太舒服。",
            "hint": "わけではない / だけ",
            "answer": "手伝いたくないわけではなく、今日は体の調子があまりよくないだけです。",
        },
        {
            "cn": "不好意思，可以请您再说明一次换班时间吗。",
            "hint": "ていただけませんか",
            "answer": "すみません、交代する時間をもう一度説明していただけませんか。",
        },
    ],
    "reading": {
        "jp": (
            "私は駅前のコンビニでアルバイトをしています。平日は授業があるので、"
            "仕事に入るのはたいてい夕方六時からです。店に着いたら、まずその日のシフトを確認し、"
            "レジの周りをきれいにしておきます。夕方はお客さんが多く、弁当や飲み物がすぐ少なくなるため、"
            "品出しも大切な仕事です。<br/><br/>"
            "先週、新しく入った後輩が、在庫の場所が分からなくて困っていました。"
            "私は全部を代わりにやるのではなく、どこを見ればいいかを説明しました。"
            "最初は時間がかかっても、自分でできるようになったほうがいいと思ったからです。"
            "仕事が終わった後、後輩に「説明が分かりやすかったです」と言われて、少し安心しました。"
        ),
        "gloss": "品出し：上货，补货 / 後輩：后辈 / 代わりに：代替，替别人",
        "questions": [
            {
                "q": "作者通常什么时候开始打工？",
                "options": ["早上六点", "下午六点", "下课前", "周末上午"],
                "answer": "下午六点",
                "explain": "文中说「仕事に入るのはたいてい夕方六時からです」。",
            },
            {
                "q": "作者到店后首先做什么？",
                "options": ["整理便当", "给店长打电话", "确认当天排班", "教后辈收银"],
                "answer": "确认当天排班",
                "explain": "文中说「まずその日のシフトを確認し」。",
            },
            {
                "q": "作者为什么没有替后辈全部做完？",
                "options": ["因为作者很忙", "因为店长不允许", "因为希望后辈自己学会", "因为库存已经足够"],
                "answer": "因为希望后辈自己学会",
                "explain": "文中说「自分でできるようになったほうがいいと思ったからです」。",
            },
            {
                "q": "读完文章，作者的态度最接近哪一个？",
                "options": ["觉得后辈很麻烦", "对说明被理解感到安心", "不想继续打工", "觉得品出し不重要"],
                "answer": "对说明被理解感到安心",
                "explain": "最后一句「少し安心しました」直接说明了作者的感受。",
            },
        ],
    },
    "output_task": {
        "prompt": "用日语写 2-3 句：如果你在便利店打工，开始工作前会提前做什么？",
        "sample": "仕事に入る前に、まずシフトを確認します。お客さんが多い時間の前に、レジの周りをきれいにしておきたいです。",
    },
}


def register_fonts():
    candidates = [
        Path("C:/Windows/Fonts/msyh.ttc"),
        Path("C:/Windows/Fonts/meiryo.ttc"),
        Path("C:/Windows/Fonts/YuGothR.ttc"),
    ]
    for font_path in candidates:
        if font_path.exists():
            pdfmetrics.registerFont(TTFont("CJK", str(font_path)))
            bold_path = Path("C:/Windows/Fonts/msyhbd.ttc")
            pdfmetrics.registerFont(TTFont("CJK-Bold", str(bold_path if bold_path.exists() else font_path)))
            return
    raise FileNotFoundError("No CJK font found.")


def styles():
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle(
            "title",
            parent=base["Title"],
            fontName="CJK-Bold",
            fontSize=20,
            leading=28,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#1f3a5f"),
            wordWrap="CJK",
        ),
        "subtitle": ParagraphStyle(
            "subtitle",
            parent=base["Normal"],
            fontName="CJK",
            fontSize=10,
            leading=15,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#586475"),
            wordWrap="CJK",
            spaceAfter=8,
        ),
        "h1": ParagraphStyle(
            "h1",
            parent=base["Heading1"],
            fontName="CJK-Bold",
            fontSize=14,
            leading=20,
            textColor=colors.HexColor("#1f3a5f"),
            wordWrap="CJK",
            spaceBefore=7,
            spaceAfter=5,
        ),
        "body": ParagraphStyle(
            "body",
            parent=base["BodyText"],
            fontName="CJK",
            fontSize=9.2,
            leading=14,
            wordWrap="CJK",
            spaceAfter=3,
        ),
        "small": ParagraphStyle(
            "small",
            parent=base["BodyText"],
            fontName="CJK",
            fontSize=8.4,
            leading=12,
            textColor=colors.HexColor("#4b5968"),
            wordWrap="CJK",
        ),
        "jp": ParagraphStyle(
            "jp",
            parent=base["BodyText"],
            fontName="CJK",
            fontSize=9.4,
            leading=15,
            wordWrap="CJK",
            firstLineIndent=8,
            spaceAfter=4,
        ),
    }


def table(data, widths, style):
    t = Table(data, colWidths=widths, repeatRows=1, hAlign="LEFT")
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e8eef5")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#1f3a5f")),
                ("GRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#d4dbe3")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 4),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#fbfcfd")]),
            ]
        )
    )
    return t


def write_markdown():
    lines = [
        f"# {UNIT['title']}：{UNIT['topic']}",
        "",
        f"目标：{UNIT['goal']}",
        "",
        "## 本单元句型",
        "",
    ]
    lines.extend([f"- {item}" for item in UNIT["focus"]])
    lines.extend(["", "## 热身词句", ""])
    for word, meaning, example in UNIT["warmup"]:
        lines.append(f"- **{word}**：{meaning}。例：{example}")
    lines.extend(["", "## 句子翻译", ""])
    for i, item in enumerate(UNIT["translations"], 1):
        lines.append(f"{i}. {item['cn']}（提示：{item['hint']}）")
    lines.extend(["", "## 阅读理解", "", UNIT["reading"]["jp"].replace("<br/><br/>", "\n\n"), "", f"词汇提示：{UNIT['reading']['gloss']}", ""])
    for i, q in enumerate(UNIT["reading"]["questions"], 1):
        lines.append(f"{i}. {q['q']}")
        for opt in q["options"]:
            lines.append(f"   - {opt}")
    lines.extend(["", "## 输出小练习", "", UNIT["output_task"]["prompt"], "", "## 参考答案", ""])
    for i, item in enumerate(UNIT["translations"], 1):
        lines.append(f"{i}. {item['answer']}")
    lines.extend(["", "### 阅读答案", ""])
    for i, q in enumerate(UNIT["reading"]["questions"], 1):
        lines.append(f"{i}. {q['answer']}。{q['explain']}")
    lines.extend(["", "### 输出参考", "", UNIT["output_task"]["sample"], ""])
    MD_PATH.write_text("\n".join(lines), encoding="utf-8")


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("CJK", 8)
    canvas.setFillColor(colors.HexColor("#6b7280"))
    canvas.drawString(17 * mm, 10 * mm, "N3 小单元训练")
    canvas.drawRightString(193 * mm, 10 * mm, str(doc.page))
    canvas.restoreState()


def build_pdf():
    register_fonts()
    st = styles()
    doc = SimpleDocTemplate(
        str(PDF_PATH),
        pagesize=A4,
        leftMargin=16 * mm,
        rightMargin=16 * mm,
        topMargin=15 * mm,
        bottomMargin=16 * mm,
        title=f"{UNIT['title']} {UNIT['topic']}",
    )
    story = [
        Paragraph(f"{UNIT['title']}：{UNIT['topic']}", st["title"]),
        Paragraph(UNIT["goal"], st["subtitle"]),
        Paragraph("本单元句型", st["h1"]),
    ]
    story.extend([Paragraph(f"- {item}", st["body"]) for item in UNIT["focus"]])

    story.append(Paragraph("热身词句", st["h1"]))
    warm_rows = [[Paragraph("词语", st["small"]), Paragraph("意思", st["small"]), Paragraph("例句", st["small"])]]
    for word, meaning, example in UNIT["warmup"]:
        warm_rows.append([Paragraph(word, st["body"]), Paragraph(meaning, st["body"]), Paragraph(example, st["body"])])
    story.append(table(warm_rows, [30 * mm, 38 * mm, 98 * mm], st))

    story.append(Paragraph("句子翻译", st["h1"]))
    trans_rows = [[Paragraph("编号", st["small"]), Paragraph("中文句子", st["small"]), Paragraph("提示", st["small"])]]
    for i, item in enumerate(UNIT["translations"], 1):
        trans_rows.append([Paragraph(str(i), st["body"]), Paragraph(item["cn"], st["body"]), Paragraph(item["hint"], st["small"])])
    story.append(table(trans_rows, [12 * mm, 108 * mm, 46 * mm], st))

    story.append(Paragraph("阅读理解", st["h1"]))
    story.append(Paragraph(UNIT["reading"]["jp"], st["jp"]))
    story.append(Paragraph(f"词汇提示：{UNIT['reading']['gloss']}", st["small"]))
    read_rows = [[Paragraph("题", st["small"]), Paragraph("问题", st["small"]), Paragraph("选项", st["small"])]]
    for i, q in enumerate(UNIT["reading"]["questions"], 1):
        options = "<br/>".join([f"{chr(64 + n)}. {opt}" for n, opt in enumerate(q["options"], 1)])
        read_rows.append([Paragraph(str(i), st["body"]), Paragraph(q["q"], st["body"]), Paragraph(options, st["small"])])
    story.append(table(read_rows, [10 * mm, 60 * mm, 96 * mm], st))

    story.append(Paragraph("输出小练习", st["h1"]))
    story.append(Paragraph(UNIT["output_task"]["prompt"], st["body"]))
    story.append(Spacer(1, 18))
    for _ in range(3):
        story.append(Paragraph("_" * 90, st["small"]))

    story.append(PageBreak())
    story.append(Paragraph("参考答案", st["h1"]))
    ans_rows = [[Paragraph("编号", st["small"]), Paragraph("参考译文", st["small"])]]
    for i, item in enumerate(UNIT["translations"], 1):
        ans_rows.append([Paragraph(str(i), st["body"]), Paragraph(item["answer"], st["body"])])
    story.append(table(ans_rows, [12 * mm, 154 * mm], st))

    story.append(Paragraph("阅读答案", st["h1"]))
    read_ans_rows = [[Paragraph("题", st["small"]), Paragraph("答案与解析", st["small"])]]
    for i, q in enumerate(UNIT["reading"]["questions"], 1):
        read_ans_rows.append([Paragraph(str(i), st["body"]), Paragraph(f"{q['answer']}。{q['explain']}", st["body"])])
    story.append(table(read_ans_rows, [12 * mm, 154 * mm], st))

    story.append(Paragraph("输出参考", st["h1"]))
    story.append(Paragraph(UNIT["output_task"]["sample"], st["body"]))
    doc.build(story, onFirstPage=footer, onLaterPages=footer)


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    write_markdown()
    build_pdf()
    print(PDF_PATH)
    print(MD_PATH)


if __name__ == "__main__":
    main()
