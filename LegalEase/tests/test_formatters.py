from document_utils.common import format_html_preview, parse_terms, sanitize_text
from document_utils.docx_formatter import format_docx
from document_utils.pdf_formatter import format_pdf
from document_utils.txt_formatter import format_txt


SAMPLE = """EMPLOYMENT AGREEMENT

This Agreement is made between Jane Doe and Example Corp.

1. CONFIDENTIALITY
The parties shall maintain confidentiality.
"""


def test_sanitize_text():
    assert sanitize_text("hello\u2014world") == "hello-world"


def test_parse_terms():
    assert parse_terms("one; two; three") == ["one", "two", "three"]


def test_html_preview():
    html = format_html_preview(SAMPLE)
    assert "<p>" in html
    assert "EMPLOYMENT AGREEMENT" in html


def test_txt():
    assert b"EMPLOYMENT AGREEMENT" in format_txt(SAMPLE)


def test_docx():
    data = format_docx(SAMPLE, "Employment Contract", "Confidentiality; Payment")
    assert data[:2] == b"PK"


def test_pdf():
    data = format_pdf(SAMPLE, "Employment Contract", "Confidentiality; Payment")
    assert data.startswith(b"%PDF")
