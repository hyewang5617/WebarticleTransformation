#!/usr/bin/env python3
"""기사 원문 텍스트를 웹기사(CKEditor 스타일) HTML로 변환한다.

입력 형식 (마크다운과 유사한 간단한 표기):
    첫 문단(리드)

    ## 소제목
    본문 문단1

    본문 문단2

    ![이미지 캡션](선택적/이미지/경로.png)

    ---
    기자명1 (직함)|이메일1
    기자명2 (직함)|이메일2

사용법:
    python convert_article.py input.txt > output.html
"""
import sys
import re

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

FONT_FAMILY = "맑은 고딕"


def smart_quotes(text: str) -> str:
    """" ' 를 여는/닫는 곡선 따옴표 엔티티로 변환한다."""
    out = []
    prev = " "
    for ch in text:
        if ch == '"':
            out.append("&ldquo;" if prev in " ([\n“‘" or prev == "" else "&rdquo;")
        elif ch == "'":
            out.append("&lsquo;" if prev in " ([\n“‘" or prev == "" else "&rsquo;")
        else:
            out.append(ch)
        prev = ch
    return "".join(out)


def convert_entities(text: str) -> str:
    text = smart_quotes(text)
    text = text.replace("“", "&ldquo;").replace("”", "&rdquo;")
    text = text.replace("‘", "&lsquo;").replace("’", "&rsquo;")
    text = text.replace("·", "&middot;")
    return text


def wrap_paragraph(text: str) -> str:
    body = convert_entities(text.strip())
    return (
        '<p><span style="font-size:14px">'
        f'<span style="font-family:{FONT_FAMILY}">&nbsp;{body}'
        "</span></span></p>"
    )


def wrap_heading(text: str) -> str:
    body = convert_entities(text.strip())
    return (
        '<p><span style="font-size:18px"><strong>'
        f'<span style="font-family:{FONT_FAMILY}">&nbsp;{body}'
        "</span></strong></span></p>\n"
        '<span style="font-size:14px">&nbsp;</span>'
    )


def wrap_image(caption: str, src: str = "") -> str:
    caption = convert_entities(caption.strip())
    return (
        '<div style="text-align:center">'
        '<span style="font-size:14px">'
        f'<span style="font-family:{FONT_FAMILY}">'
        f'<img alt="" src="{src}" style="height:400px; width:750px" />'
        "</span><br />\n"
        '<span style="font-size:12px"><strong>&#9650; '
        f"{caption}</strong></span></span><br />\n"
        "&nbsp;</div>"
    )


def wrap_byline(entries) -> str:
    lines = []
    for name, email in entries:
        lines.append(convert_entities(name.strip()))
        lines.append(email.strip())
    joined = "<br />\n".join(lines)
    return (
        '<p style="text-align:right"><strong>'
        '<span style="font-size:14px">'
        f'<span style="font-family:{FONT_FAMILY}">{joined}'
        "</span></span></strong></p>"
    )


def convert(source: str) -> str:
    # 문단 단위(빈 줄)로 블록 분리
    raw_blocks = [b.strip() for b in re.split(r"\n\s*\n", source.strip()) if b.strip()]

    html_parts = []
    in_byline = False
    byline_entries = []

    for block in raw_blocks:
        lines = block.splitlines()

        if in_byline or lines[0].strip() == "---":
            if lines[0].strip() == "---":
                in_byline = True
                lines = lines[1:]
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                name, _, email = line.partition("|")
                byline_entries.append((name, email))
            continue

        if block.startswith("## "):
            html_parts.append(wrap_heading(block[3:]))
            continue

        m = re.match(r"^!\[(.*?)\]\((.*?)\)\s*$", block)
        if m:
            html_parts.append(wrap_image(m.group(1), m.group(2)))
            continue
        m = re.match(r"^!\[(.*?)\]\s*$", block)
        if m:
            html_parts.append(wrap_image(m.group(1)))
            continue

        # 일반 문단: 블록 내 개별 줄(화자 교체 등)은 각각 별도 <p>로 처리
        for para in block.split("\n"):
            para = para.strip()
            if para:
                html_parts.append(wrap_paragraph(para))

    if byline_entries:
        html_parts.append(wrap_byline(byline_entries))

    return "\n\n".join(html_parts) + "\n"


def main():
    if len(sys.argv) != 2:
        print("사용법: python convert_article.py <input.txt>", file=sys.stderr)
        sys.exit(1)

    with open(sys.argv[1], "r", encoding="utf-8") as f:
        source = f.read()

    sys.stdout.write(convert(source))


if __name__ == "__main__":
    main()
