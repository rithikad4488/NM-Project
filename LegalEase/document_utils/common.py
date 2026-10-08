import html
import re
from pathlib import Path
from typing import List


def sanitize_text(text: str) -> str:
    """Normalize text for reliable document export."""
    if not text:
        return ""

    replacements = {
        "\u2018": "'",
        "\u2019": "'",
        "\u201c": '"',
        "\u201d": '"',
        "\u2013": "-",
        "\u2014": "-",
        "\u2026": "...",
        "\u00a0": " ",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)

    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def parse_terms(terms: str) -> List[str]:
    return [item.strip() for item in terms.split(";") if item.strip()]


def format_html_preview(text: str) -> str:
    """Convert plain generated text into safe HTML for Streamlit preview."""
    safe = html.escape(sanitize_text(text))
    paragraphs = []
    for block in safe.split("\n\n"):
        lines = block.splitlines()
        if not lines:
            continue

        if len(lines) == 1 and len(lines[0]) < 100 and (
            lines[0].isupper()
            or re.match(r"^\d+[\.\)]\s+", lines[0])
        ):
            paragraphs.append(f"<h3>{lines[0]}</h3>")
        else:
            paragraphs.append(
                "<p>" + "<br>".join(lines) + "</p>"
            )

    return "\n".join(paragraphs)


def logo_path() -> Path | None:
    path = Path(__file__).resolve().parent.parent / "assets" / "logo.png"
    return path if path.exists() else None
