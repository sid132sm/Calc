#!/usr/bin/env python3
"""Render the companion Markdown guide as a simple, dependency-free PDF."""

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "PROJECT_LEARNING_GUIDE.md"
OUTPUT = ROOT / "Calculator_Project_Learning_Guide.pdf"

PAGE_WIDTH, PAGE_HEIGHT = 612, 792  # US Letter, in PDF points
LEFT, RIGHT, TOP, BOTTOM = 54, 54, 54, 48
BODY_SIZE, CODE_SIZE = 9.4, 8.1
LEADING, CODE_LEADING = 13, 11


def esc(value: str) -> str:
    return value.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def ascii_text(value: str) -> str:
    return (value.replace("→", "->").replace("×", "x").replace("÷", "/")
            .replace("**", "").replace("`", "").encode("latin-1", "replace").decode("latin-1"))


def wrap(text: str, width: int) -> list[str]:
    words = text.split()
    if not words:
        return [""]
    result, line = [], ""
    for word in words:
        if not line:
            line = word
        elif len(line) + len(word) + 1 <= width:
            line += " " + word
        else:
            result.append(line)
            line = word
    result.append(line)
    return result


def parse_markdown(markdown: str):
    blocks, paragraph, code, in_code = [], [], [], False

    def flush_paragraph():
        nonlocal paragraph
        if paragraph:
            blocks.append(("body", " ".join(paragraph)))
            paragraph = []

    for raw in markdown.splitlines():
        line = raw.rstrip()
        if line.startswith("```"):
            flush_paragraph()
            if in_code:
                blocks.append(("code", code))
                code = []
            in_code = not in_code
        elif in_code:
            code.append(line)
        elif not line.strip():
            flush_paragraph()
        elif line.startswith("# "):
            flush_paragraph(); blocks.append(("title", line[2:]))
        elif line.startswith("## "):
            flush_paragraph(); blocks.append(("h1", line[3:]))
        elif line.startswith("### "):
            flush_paragraph(); blocks.append(("h2", line[4:]))
        elif line.startswith("- "):
            flush_paragraph(); blocks.append(("bullet", line[2:]))
        elif re.match(r"\d+\. ", line):
            flush_paragraph(); blocks.append(("bullet", line))
        else:
            paragraph.append(line)
    flush_paragraph()
    return blocks


def make_pages(blocks):
    pages, page, y = [], [], PAGE_HEIGHT - TOP

    def new_page():
        nonlocal page, y
        if page:
            pages.append(page)
        page, y = [], PAGE_HEIGHT - TOP

    def add(kind, text, size, leading, indent=0):
        nonlocal y
        if y - leading < BOTTOM:
            new_page()
        page.append((kind, LEFT + indent, y, size, text))
        y -= leading

    for kind, content in blocks:
        if kind == "title":
            if y < PAGE_HEIGHT - TOP - 12:
                new_page()
            add("bold", ascii_text(content), 22, 30)
            add("body", "A guided explanation of the React + Django calculator", 11, 22)
        elif kind == "h1":
            y -= 8
            add("bold", ascii_text(content), 15, 22)
        elif kind == "h2":
            y -= 4
            add("bold", ascii_text(content), 11.5, 17)
        elif kind == "body":
            for line in wrap(ascii_text(content), 92):
                add("body", line, BODY_SIZE, LEADING)
            y -= 4
        elif kind == "bullet":
            lines = wrap(ascii_text(content), 84)
            for index, line in enumerate(lines):
                add("body", ("- " if index == 0 else "  ") + line, BODY_SIZE, LEADING, 10)
            y -= 2
        elif kind == "code":
            for line in content:
                for part in wrap(ascii_text(line), 91):
                    add("code", part, CODE_SIZE, CODE_LEADING, 8)
            y -= 6
    if page:
        pages.append(page)
    return pages


def pdf_bytes(pages):
    objects = []
    # 1 catalog, 2 pages tree, 3 regular font, 4 bold font
    objects.extend(["<< /Type /Catalog /Pages 2 0 R >>", "", "<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>", "<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >>"])
    page_ids = []
    for page_num, page in enumerate(pages, 1):
        commands = ["BT"]
        for kind, x, y, size, text in page:
            font = "F2" if kind == "bold" else "F3" if kind == "code" else "F1"
            commands.append(f"/{font} {size} Tf 1 0 0 1 {x:.1f} {y:.1f} Tm ({esc(text)}) Tj")
        commands.append(f"/F1 8 Tf 1 0 0 1 {LEFT} 24 Tm (Calculator Project Learning Guide | Page {page_num} of {len(pages)}) Tj")
        commands.append("ET")
        stream = "\n".join(commands)
        content_id = len(objects) + 1
        objects.append(f"<< /Length {len(stream.encode('latin-1'))} >>\nstream\n{stream}\nendstream")
        page_id = len(objects) + 1
        page_ids.append(page_id)
        objects.append(f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 {PAGE_WIDTH} {PAGE_HEIGHT}] /Resources << /Font << /F1 3 0 R /F2 4 0 R /F3 3 0 R >> >> /Contents {content_id} 0 R >>")
    objects[1] = f"<< /Type /Pages /Kids [{' '.join(f'{page} 0 R' for page in page_ids)}] /Count {len(page_ids)} >>"
    result = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offsets = [0]
    for index, obj in enumerate(objects, 1):
        offsets.append(len(result))
        result.extend(f"{index} 0 obj\n{obj}\nendobj\n".encode("latin-1"))
    startxref = len(result)
    result.extend(f"xref\n0 {len(objects) + 1}\n0000000000 65535 f \n".encode())
    for offset in offsets[1:]:
        result.extend(f"{offset:010d} 00000 n \n".encode())
    result.extend(f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\nstartxref\n{startxref}\n%%EOF\n".encode())
    return bytes(result)


if __name__ == "__main__":
    pages = make_pages(parse_markdown(SOURCE.read_text(encoding="utf-8")))
    OUTPUT.write_bytes(pdf_bytes(pages))
    print(f"Wrote {OUTPUT} ({len(pages)} pages)")
