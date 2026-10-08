import os
from typing import Optional

from dotenv import load_dotenv

load_dotenv()

try:
    import google.generativeai as genai
except ImportError:  # pragma: no cover
    genai = None


class GeminiDocumentGenerator:
    """Small, testable wrapper around the Google Gemini SDK."""

    def __init__(self, api_key: Optional[str] = None, model_name: Optional[str] = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY", "").strip()
        self.model_name = model_name or os.getenv(
            "GEMINI_MODEL", "gemini-1.5-pro"
        ).strip()

    def _model(self):
        if not self.api_key:
            raise RuntimeError(
                "GEMINI_API_KEY is missing. Add it to the .env file."
            )
        if genai is None:
            raise RuntimeError(
                "google-generativeai is not installed. Run pip install -r requirements.txt."
            )

        genai.configure(api_key=self.api_key)
        return genai.GenerativeModel(
            model_name=self.model_name,
            generation_config={
                "temperature": 0.25,
                "top_p": 0.9,
                "max_output_tokens": 8192,
            },
        )

    @staticmethod
    def build_prompt(
        document_type: str,
        parties: str,
        terms: str,
        effective_date: str,
    ) -> str:
        term_items = [
            item.strip() for item in terms.split(";") if item.strip()
        ]
        terms_text = "\n".join(f"- {item}" for item in term_items)

        return f"""
You are LegalEase, an AI-assisted legal document drafting engine.

Create a professional legal document based ONLY on the user-provided facts.
Do not invent names, addresses, amounts, dates, obligations, governing laws,
or other material facts.

DOCUMENT TYPE:
{document_type}

PARTIES:
{parties}

EFFECTIVE DATE:
{effective_date}

USER-SUPPLIED TERMS:
{terms_text}

Writing requirements:
1. Use a clear formal legal-document structure.
2. Include a title.
3. Include a parties/introduction section.
4. Include numbered sections with useful headings.
5. Incorporate every supplied term without changing its meaning.
6. If an important fact is missing, use a neutral placeholder such as
   [INSERT DETAILS] instead of inventing it.
7. End with signature blocks appropriate for the parties.
8. Do not include markdown code fences.
9. Do not claim the document is legally valid, lawyer-approved, or jurisdiction-specific.
10. Keep the result editable plain text.

Return ONLY the document text.
""".strip()

    def generate_document(
        self,
        document_type: str,
        parties: str,
        terms: str,
        effective_date: str,
    ) -> str:
        prompt = self.build_prompt(
            document_type=document_type,
            parties=parties,
            terms=terms,
            effective_date=effective_date,
        )

        try:
            response = self._model().generate_content(prompt)
        except Exception as exc:
            raise RuntimeError(f"Gemini request failed: {exc}") from exc

        text = getattr(response, "text", None)
        if not text:
            raise RuntimeError(
                "Gemini returned an empty response. Check the model name and API key."
            )

        return text.strip()
