import io
import re
from docx import Document


def add_formatted_paragraph(doc, text, style='Normal'):
    """Parses inline bold syntax (**text**) and adds it to a Word paragraph."""
    p = doc.add_paragraph(style=style)
    # Split text by bold syntax while keeping delimiters
    tokens = re.split(r'(\*\*.*?\*\*)', text)

    for token in tokens:
        if token.startswith('**') and token.endswith('**'):
            # Strip the ** markers and apply bold style
            run = p.add_run(token[2:-2])
            run.bold = True
        else:
            p.add_run(token)
    return p


def convert_to_docx(text: str) -> bytes:
    doc = Document()

    for line in text.split("\n"):
        line_str = line.strip()
        if not line_str:
            continue  # Skip blank lines

        # Parse Headers
        if line_str.startswith("# "):
            doc.add_heading(line_str[2:], level=1)
        elif line_str.startswith("## "):
            doc.add_heading(line_str[3:], level=2)
        elif line_str.startswith("### "):
            doc.add_heading(line_str[4:], level=3)
        # Parse Bullet Points
        elif line_str.startswith("- ") or line_str.startswith("* "):
            add_formatted_paragraph(doc, line_str[2:], style='List Bullet')
        # Standard Paragraphs & Bold Text
        else:
            add_formatted_paragraph(doc, line_str, style='Normal')

    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer.getvalue()