from __future__ import annotations

import json
import re
from pathlib import Path

from docx import Document


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "形测题库.docx"
OUT_MD = ROOT / "output" / "形测题库_整理.md"
OUT_JSON = ROOT / "output" / "形测题库_整理.json"

TYPE_RE = re.compile(r"(单选题|多选题)\s*\(\s*(\d+)\s*分\s*\)")
SCORE_RE = re.compile(r"(\d+)\s*分")
NUMBER_RE = re.compile(r"^\d+\.$")
OPTION_RE = re.compile(r"^[A-D]\.?$")
RED = "FF0000"


def clean(text: str) -> str:
    return re.sub(r"\s+", " ", text.replace("\xa0", " ")).strip()


def paragraph_is_red(paragraph) -> bool:
    runs = [run for run in paragraph.runs if run.text.strip()]
    if not runs:
        return False
    return any(str(run.font.color.rgb) == RED for run in runs if run.font.color.rgb)


def split_question_type(text: str) -> tuple[str, str | None]:
    match = TYPE_RE.search(text)
    if not match:
        return text, None
    question = text[: match.start()].strip()
    type_line = text[match.start() :].strip()
    return question, type_line


def parse_type_and_score(type_line: str, next_line: str | None = None) -> tuple[str, int, int | None, bool]:
    match = TYPE_RE.search(type_line)
    if not match:
        raise ValueError(f"Cannot parse question type from: {type_line}")

    qtype = match.group(1)
    total = int(match.group(2))
    tail = type_line[match.end() :]
    score_match = SCORE_RE.search(tail)
    consumed_next = False
    if not score_match and next_line:
        score_match = SCORE_RE.fullmatch(next_line.strip())
        consumed_next = bool(score_match)

    score = int(score_match.group(1)) if score_match else None
    return qtype, total, score, consumed_next


def parse_questions():
    doc = Document(SOURCE)
    lines = [
        {"text": clean(p.text), "red": paragraph_is_red(p)}
        for p in doc.paragraphs
        if clean(p.text)
    ]

    questions = []
    i = 0
    serial = 1
    while i < len(lines):
        original_number = None
        if NUMBER_RE.fullmatch(lines[i]["text"]):
            original_number = int(lines[i]["text"][:-1])
            i += 1
            if i >= len(lines):
                break

        question_parts = []
        type_line = None
        while i < len(lines):
            text = lines[i]["text"]
            question_text, embedded_type = split_question_type(text)
            if embedded_type:
                if question_text:
                    question_parts.append(question_text)
                type_line = embedded_type
                i += 1
                break
            if TYPE_RE.search(text):
                type_line = text
                i += 1
                break
            question_parts.append(text)
            i += 1

        if not type_line:
            break

        next_text = lines[i]["text"] if i < len(lines) else None
        qtype, total_score, score, consumed_next = parse_type_and_score(type_line, next_text)
        if consumed_next:
            i += 1

        options = []
        while i < len(lines):
            text = lines[i]["text"]
            if NUMBER_RE.fullmatch(text) and len(options) >= 4:
                break
            if not OPTION_RE.fullmatch(text):
                # Stray content after a complete option block usually means the next question
                # was copied without a number; keep parsing conservative.
                if len(options) >= 4:
                    break
                i += 1
                continue

            letter = text[0]
            marker_red = lines[i]["red"]
            i += 1
            option_text = lines[i]["text"] if i < len(lines) else ""
            option_red = lines[i]["red"] if i < len(lines) else False
            if i < len(lines):
                i += 1
            options.append(
                {
                    "letter": letter,
                    "text": option_text,
                    "marked_red": marker_red or option_red,
                }
            )

        marked = [opt["letter"] for opt in options if opt["marked_red"]]
        answer = marked if score == total_score and marked else []
        questions.append(
            {
                "id": serial,
                "original_number": original_number or serial,
                "question": " ".join(question_parts).strip(),
                "type": qtype,
                "total_score": total_score,
                "recorded_score": score,
                "options": options,
                "marked_red": marked,
                "answer": answer,
                "answer_status": "confirmed_from_full_score" if answer else "needs_verification",
            }
        )
        serial += 1

    return questions


def markdown_for(questions) -> str:
    confirmed = sum(1 for q in questions if q["answer_status"] == "confirmed_from_full_score")
    pending = len(questions) - confirmed
    lines = [
        "# 形测题库整理版",
        "",
        f"- 来源：`{SOURCE.name}`",
        f"- 题目总数：{len(questions)}",
        f"- 已确认答案：{confirmed}",
        f"- 待核对答案：{pending}",
        "",
        "> 说明：原 Word 中红色字体表示被标记/选择的选项。满分题的红色选项已整理为答案；0 分或未记录满分的题只保留红色标记，答案状态为“待核对”。",
        "",
    ]

    for q in questions:
        status = "已确认" if q["answer_status"] == "confirmed_from_full_score" else "待核对"
        answer = "".join(q["answer"]) if q["answer"] else "待核对"
        marked = "".join(q["marked_red"]) if q["marked_red"] else "无"
        lines.extend(
            [
                f"## {q['id']}. {q['question']}",
                "",
                f"- 原编号：{q['original_number']}",
                f"- 题型：{q['type']}（{q['total_score']} 分）",
                f"- 记录得分：{q['recorded_score'] if q['recorded_score'] is not None else '未记录'}",
                f"- 答案：{answer}（{status}）",
                f"- 红色标记：{marked}",
                "",
            ]
        )
        for opt in q["options"]:
            marker = " [红色]" if opt["marked_red"] else ""
            lines.append(f"{opt['letter']}. {opt['text']}{marker}")
        lines.append("")

    return "\n".join(lines)


def main() -> None:
    questions = parse_questions()
    OUT_MD.parent.mkdir(parents=True, exist_ok=True)
    OUT_MD.write_text(markdown_for(questions), encoding="utf-8-sig")
    OUT_JSON.write_text(json.dumps(questions, ensure_ascii=False, indent=2), encoding="utf-8")

    confirmed = sum(1 for q in questions if q["answer_status"] == "confirmed_from_full_score")
    pending = len(questions) - confirmed
    print(f"questions={len(questions)} confirmed={confirmed} pending={pending}")
    print(f"markdown={OUT_MD}")
    print(f"json={OUT_JSON}")


if __name__ == "__main__":
    main()
