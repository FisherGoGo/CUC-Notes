from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import uuid
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORK_ROOT = ROOT / "tmp" / "xelatex_pdf"


def latex_escape_text(text: str) -> str:
    replacements = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    return "".join(replacements.get(ch, ch) for ch in text)


def render_text_markup(text: str) -> str:
    parts = re.split(r"(`[^`]*`|\*\*[^*]+\*\*)", text)
    rendered: list[str] = []
    for part in parts:
        if not part:
            continue
        if part.startswith("`") and part.endswith("`"):
            rendered.append(r"\texttt{" + latex_escape_text(part[1:-1]) + "}")
        elif part.startswith("**") and part.endswith("**"):
            rendered.append(r"\textbf{" + latex_escape_text(part[2:-2]) + "}")
        else:
            rendered.append(latex_escape_text(part))
    return "".join(rendered)


def render_inline(text: str) -> str:
    # 只在非数学片段里转义特殊字符，避免破坏 $...$ 里的 LaTeX 公式。
    parts = re.split(r"(\$[^$\n]+\$)", text)
    rendered: list[str] = []
    for part in parts:
        if not part:
            continue
        if part.startswith("$") and part.endswith("$"):
            rendered.append(part)
        else:
            rendered.append(render_text_markup(part))
    return "".join(rendered)


def heading(level: int, text: str) -> str:
    commands = {
        1: "section*",
        2: "subsection*",
        3: "subsubsection*",
        4: "paragraph",
    }
    command = commands.get(level, "paragraph")
    return rf"\{command}{{{render_inline(text)}}}"


def item_line(text: str) -> str:
    indent = len(text) - len(text.lstrip(" \t"))
    stripped = text.strip()
    level = max(0, indent // 2)
    numbered = re.match(r"^(\d+\.)\s+(.+)$", stripped)
    if numbered:
        return rf"\noindent\hspace*{{{level * 1.2}em}}{numbered.group(1)}\ {render_inline(numbered.group(2))}\par"
    clean = re.sub(r"^[-*]\s+", "", stripped)
    return rf"\noindent\hspace*{{{level * 1.2}em}}\textbullet\ {render_inline(clean)}\par"


def quote_line(text: str) -> str:
    clean = text[1:].strip()
    clean = re.sub(r"^\[!([A-Z]+)\]-?\s*$", r"\\textbf{\1}", clean)
    return rf"\begin{{quote}}\small {render_inline(clean)}\end{{quote}}"


def table_to_latex(lines: list[str]) -> list[str]:
    rows = []
    for line in lines:
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if cells and all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells):
            continue
        rows.append(cells)
    if not rows:
        return []
    col_count = max(len(row) for row in rows)
    spec = "p{0.22\\linewidth}" * col_count
    out = [r"\begin{longtable}{" + spec + "}"]
    for idx, row in enumerate(rows):
        row = row + [""] * (col_count - len(row))
        out.append(" & ".join(render_inline(cell) for cell in row) + r" \\")
        if idx == 0:
            out.append(r"\midrule")
    out.append(r"\end{longtable}")
    return out


def markdown_to_latex(md: str, title: str) -> str:
    lines = md.splitlines()
    body: list[str] = []
    in_display_math = False
    table_buffer: list[str] = []

    def flush_table() -> None:
        nonlocal table_buffer
        if table_buffer:
            body.extend(table_to_latex(table_buffer))
            table_buffer = []

    for raw in lines:
        line = raw.rstrip()
        stripped = line.strip()

        if not body and stripped.startswith("# "):
            continue

        if stripped.startswith("|") and stripped.endswith("|") and not in_display_math:
            table_buffer.append(line)
            continue
        flush_table()

        if stripped.startswith(">") and not in_display_math:
            line = stripped[1:].strip()
            stripped = line.strip()
            callout = re.match(r"^\[!([A-Z]+)\]-?\s*(.*)$", stripped)
            if callout:
                label = callout.group(1)
                rest = callout.group(2).strip()
                callout_title = f"{label}: {rest}" if rest else label
                body.append(r"\textbf{" + latex_escape_text(callout_title) + r"}\par")
                continue

        if in_display_math:
            math_line = line.strip()[1:].strip() if line.strip().startswith(">") else line
            if math_line.strip() == "$$":
                body.append(r"\]")
                in_display_math = False
            else:
                body.append(math_line)
            continue
        if stripped == "$$":
            body.append(r"\[")
            in_display_math = True
            continue
        if not stripped:
            body.append("")
            continue

        match = re.match(r"^(#{1,4})\s+(.+)$", stripped)
        if match:
            body.append(heading(len(match.group(1)), match.group(2)))
            continue
        if re.match(r"^\s*([-*]\s+|\d+\.\s+)", line):
            body.append(item_line(line))
            continue

        body.append(render_inline(stripped) + r"\par")

    flush_table()

    return rf"""
\documentclass[11pt,a4paper]{{ctexart}}
\usepackage{{amsmath,amssymb,mathtools}}
\usepackage{{geometry}}
\usepackage{{enumitem}}
\usepackage{{booktabs,longtable,array}}
\usepackage{{xcolor}}
\usepackage{{hyperref}}
\usepackage{{fancyhdr}}
\geometry{{left=22mm,right=22mm,top=20mm,bottom=22mm}}
\setCJKmainfont{{SimSun}}
\setCJKsansfont{{Microsoft YaHei}}
\setmainfont{{SimSun}}
\linespread{{1.18}}
\setlength{{\parindent}}{{0pt}}
\setlength{{\parskip}}{{0.45em}}
\hypersetup{{colorlinks=true,linkcolor=blue,urlcolor=blue}}
\pagestyle{{fancy}}
\fancyhf{{}}
\fancyfoot[C]{{{render_inline(title)} · \thepage}}
\renewcommand{{\headrulewidth}}{{0pt}}
\title{{{render_inline(title)}}}
\author{{}}
\date{{}}
\begin{{document}}
\maketitle
{chr(10).join(body)}
\end{{document}}
""".lstrip()


def build_pdf(md_path: Path, pdf_path: Path) -> None:
    md_path = md_path.resolve()
    pdf_path = pdf_path.resolve()
    md = md_path.read_text(encoding="utf-8")
    first_heading = next((line[2:].strip() for line in md.splitlines() if line.startswith("# ")), md_path.stem)
    work_name = re.sub(r"[^A-Za-z0-9_-]+", "_", md_path.stem)
    work_dir = WORK_ROOT / f"{work_name}_{uuid.uuid4().hex[:8]}"
    work_dir.mkdir(parents=True, exist_ok=True)
    tex_path = work_dir / "document.tex"
    tex_path.write_text(markdown_to_latex(md, first_heading), encoding="utf-8", newline="\n")
    subprocess.run(
        ["xelatex", "-interaction=nonstopmode", "-halt-on-error", "document.tex"],
        cwd=work_dir,
        check=True,
    )
    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(work_dir / "document.pdf", pdf_path)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("output")
    args = parser.parse_args()
    build_pdf(ROOT / args.input, ROOT / args.output)
    print((ROOT / args.output).resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
