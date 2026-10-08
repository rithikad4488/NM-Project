from io import BytesIO

from fpdf import FPDF

from document_utils.common import logo_path, parse_terms, sanitize_text


class LegalEasePDF(FPDF):
    def __init__(self, doc_type: str):
        super().__init__()
        self.doc_type = doc_type

    def header(self):
        logo = logo_path()
        if logo:
            try:
                self.image(str(logo), x=90, y=8, w=30)
                self.ln(22)
            except Exception:
                self.ln(5)
        else:
            self.ln(5)

        self.set_font("Times", "B", 14)
        self.cell(0, 8, sanitize_text(self.doc_type), align="C")
        self.ln(12)

    def footer(self):
        self.set_y(-15)
        self.set_font("Times", "I", 8)
        self.cell(
            0,
            10,
            "LegalEase - AI-assisted draft | Review with a qualified legal professional",
            align="C",
        )


def format_pdf(
    text: str,
    doc_type: str,
    terms: str = "",
) -> bytes:
    pdf = LegalEasePDF(doc_type)
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()

    for block in sanitize_text(text).split("\n\n"):
        block = block.strip()
        if not block:
            continue

        lines = block.splitlines()
        if len(lines) == 1 and (
            lines[0].isupper() or lines[0][:3].isdigit()
        ):
            pdf.set_font("Times", "B", 12)
            pdf.multi_cell(0, 7, lines[0])
            pdf.ln(2)
        else:
            pdf.set_font("Times", "", 11)
            pdf.multi_cell(0, 6, "\n".join(lines))
            pdf.ln(3)

    parsed_terms = parse_terms(terms)
    if parsed_terms:
        pdf.set_font("Times", "B", 12)
        pdf.cell(0, 8, "KEY TERMS")
        pdf.ln(9)
        pdf.set_font("Times", "", 10)
        for index, term in enumerate(parsed_terms, start=1):
            pdf.multi_cell(0, 6, f"{index}. {term}")
            pdf.ln(1)

    raw = pdf.output()
    if isinstance(raw, str):
        raw = raw.encode("latin-1")
    return bytes(raw)
