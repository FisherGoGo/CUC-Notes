from __future__ import annotations

import re
import sys
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer


ROOT = Path(__file__).resolve().parents[1]
FONT_DIR = Path("C:/Windows/Fonts")


def register_fonts() -> tuple[str, str]:
    body_font = FONT_DIR / "simsun.ttc"
    bold_font = FONT_DIR / "simhei.ttf"
    fallback_font = FONT_DIR / "simfang.ttf"

    if body_font.exists():
        pdfmetrics.registerFont(TTFont("CNBody", str(body_font), subfontIndex=0))
    elif fallback_font.exists():
        pdfmetrics.registerFont(TTFont("CNBody", str(fallback_font)))
    else:
        raise FileNotFoundError("No Chinese body font found under C:/Windows/Fonts")

    if bold_font.exists():
        pdfmetrics.registerFont(TTFont("CNBold", str(bold_font)))
    else:
        pdfmetrics.registerFont(TTFont("CNBold", "CNBody"))

    return "CNBody", "CNBold"


def escape(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def inline_markdown(text: str) -> str:
    text = escape(text)
    text = re.sub(r"`([^`]+)`", r"<font name='Courier'>\1</font>", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", text)
    return text


def page_footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("CNBody", 8)
    canvas.setFillColor(colors.HexColor("#666666"))
    footer_title = getattr(doc, "display_title", "观星复习材料")
    canvas.drawCentredString(A4[0] / 2, 10 * mm, f"{footer_title} · {doc.page}")
    canvas.restoreState()


def build_pdf(md_path: Path, pdf_path: Path) -> None:
    body_font, bold_font = register_fonts()
    md_lines = md_path.read_text(encoding="utf-8").splitlines()
    display_title = next(
        (line[2:].strip() for line in md_lines if line.startswith("# ")),
        pdf_path.stem,
    )

    styles = getSampleStyleSheet()
    base = ParagraphStyle(
        "CNBase",
        parent=styles["Normal"],
        fontName=body_font,
        fontSize=9.4,
        leading=14,
        wordWrap="CJK",
        alignment=TA_LEFT,
        spaceAfter=4,
    )
    normal = base
    quote = ParagraphStyle(
        "Quote",
        parent=base,
        leftIndent=7 * mm,
        rightIndent=4 * mm,
        textColor=colors.HexColor("#555555"),
        backColor=colors.HexColor("#F5F7FA"),
        borderPadding=5,
        spaceBefore=2,
        spaceAfter=7,
    )
    h1 = ParagraphStyle(
        "H1",
        parent=base,
        fontName=bold_font,
        fontSize=18,
        leading=24,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#1F2937"),
        spaceAfter=9,
    )
    h2 = ParagraphStyle(
        "H2",
        parent=base,
        fontName=bold_font,
        fontSize=13,
        leading=18,
        textColor=colors.HexColor("#1D4ED8"),
        spaceBefore=8,
        spaceAfter=5,
        keepWithNext=True,
    )
    h3 = ParagraphStyle(
        "H3",
        parent=base,
        fontName=bold_font,
        fontSize=10.6,
        leading=15,
        textColor=colors.HexColor("#111827"),
        spaceBefore=5,
        spaceAfter=3,
        keepWithNext=True,
    )
    item = ParagraphStyle(
        "Item",
        parent=base,
        leftIndent=5 * mm,
        firstLineIndent=-5 * mm,
        spaceBefore=3,
        spaceAfter=4,
        keepWithNext=True,
    )
    answer = ParagraphStyle(
        "Answer",
        parent=base,
        leftIndent=8 * mm,
        firstLineIndent=-3 * mm,
        textColor=colors.HexColor("#111827"),
        spaceAfter=2,
    )
    note = ParagraphStyle(
        "Note",
        parent=base,
        leftIndent=6 * mm,
        firstLineIndent=-4 * mm,
        textColor=colors.HexColor("#374151"),
    )

    doc = SimpleDocTemplate(
        str(pdf_path),
        pagesize=A4,
        leftMargin=17 * mm,
        rightMargin=17 * mm,
        topMargin=15 * mm,
        bottomMargin=17 * mm,
        title=display_title,
        author="Codex",
    )
    doc.display_title = display_title

    story = []
    for raw in md_lines:
        line = raw.rstrip()
        if not line:
            story.append(Spacer(1, 2))
            continue
        if line.startswith("# "):
            story.append(Paragraph(inline_markdown(line[2:]), h1))
            continue
        if line.startswith("## "):
            if story:
                story.append(Spacer(1, 4))
            story.append(Paragraph(inline_markdown(line[3:]), h2))
            continue
        if line.startswith("### "):
            story.append(Paragraph(inline_markdown(line[4:]), h3))
            continue
        if line.startswith("> "):
            story.append(Paragraph(inline_markdown(line[2:]), quote))
            continue
        stripped = line.strip()
        if re.match(r"^\d+\.\s", stripped):
            story.append(Paragraph(inline_markdown(stripped), item))
            continue
        if stripped.startswith("- "):
            story.append(Paragraph("• " + inline_markdown(stripped[2:]), note))
            continue
        if stripped.startswith("答案："):
            story.append(Paragraph("<b>答案：</b>" + inline_markdown(stripped[3:]), answer))
            continue
        if stripped.startswith("解析："):
            story.append(Paragraph("<b>解析：</b>" + inline_markdown(stripped[3:]), answer))
            continue
        story.append(Paragraph(inline_markdown(stripped), normal))

    doc.build(story, onFirstPage=page_footer, onLaterPages=page_footer)


def main() -> int:
    if len(sys.argv) != 3:
        print("Usage: python tools/md_to_print_pdf.py input.md output.pdf", file=sys.stderr)
        return 2
    md_path = (ROOT / sys.argv[1]).resolve()
    pdf_path = (ROOT / sys.argv[2]).resolve()
    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    build_pdf(md_path, pdf_path)
    print(pdf_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
