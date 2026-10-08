import os
from datetime import date

import requests
import streamlit as st
from dotenv import load_dotenv

from document_utils.common import format_html_preview
from document_utils.docx_formatter import format_docx
from document_utils.pdf_formatter import format_pdf
from document_utils.txt_formatter import format_txt

load_dotenv()

BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000").rstrip("/")

st.set_page_config(
    page_title="LegalEase",
    page_icon="⚖️",
    layout="wide",
)

st.markdown(
    """
    <style>
    .main-title { text-align:center; font-size:42px; font-weight:700; margin-bottom:0; }
    .subtitle { text-align:center; color:#888; margin-bottom:25px; }
    .preview {
        background:#171717; color:#f4f4f4; padding:28px;
        border-radius:14px; max-height:650px; overflow-y:auto;
        border:1px solid #333; line-height:1.65;
    }
    .preview h3 { color:#fff; margin-top:18px; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="main-title">⚖️ LegalEase</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">AI-Powered Legal Document Generator</div>',
    unsafe_allow_html=True,
)

with st.sidebar:
    st.header("Document Details")
    document_type = st.selectbox(
        "Document Type",
        [
            "Employment Contract",
            "Non-Disclosure Agreement (NDA)",
            "Lease Agreement",
            "Employment Offer Letter",
            "Service Agreement",
            "Freelance Work Contract",
            "Custom Agreement",
        ],
    )
    if document_type == "Custom Agreement":
        document_type = st.text_input(
            "Custom document type",
            placeholder="e.g. Partnership Agreement",
        )

    parties = st.text_area(
        "Parties Involved",
        placeholder="Jane Doe (Service Provider), TechNova Inc. (Client)",
        height=100,
    )
    terms = st.text_area(
        "Terms & Conditions",
        placeholder=(
            "Payment within 30 days; Confidentiality must be maintained; "
            "Either party may terminate with 15 days notice"
        ),
        height=150,
        help="Separate each term with a semicolon (;).",
    )
    effective_date = st.date_input(
        "Effective Date",
        value=date.today(),
    )

    generate = st.button(
        "✨ Generate Document",
        type="primary",
        use_container_width=True,
    )

if "document" not in st.session_state:
    st.session_state.document = ""
if "generated_type" not in st.session_state:
    st.session_state.generated_type = ""

if generate:
    if not document_type.strip():
        st.error("Please enter a document type.")
    elif not parties.strip():
        st.error("Please enter the parties involved.")
    elif not terms.strip():
        st.error("Please enter at least one term.")
    else:
        payload = {
            "document_type": document_type.strip(),
            "parties": parties.strip(),
            "terms": terms.strip(),
            "effective_date": effective_date.isoformat(),
        }
        with st.spinner("Generating your document with Gemini..."):
            try:
                response = requests.post(
                    f"{BACKEND_URL}/generate",
                    json=payload,
                    timeout=120,
                )
                if response.ok:
                    data = response.json()
                    st.session_state.document = data["content"]
                    st.session_state.generated_type = document_type
                    st.success("Document generated successfully.")
                else:
                    try:
                        detail = response.json().get("detail", response.text)
                    except Exception:
                        detail = response.text
                    st.error(f"Backend error: {detail}")
            except requests.RequestException as exc:
                st.error(
                    "Could not connect to FastAPI. Start the backend first. "
                    f"Details: {exc}"
                )

st.subheader("Document Preview")

if st.session_state.document:
    tab_preview, tab_edit = st.tabs(["Preview", "Edit Document"])

    with tab_preview:
        preview_html = format_html_preview(st.session_state.document)
        st.markdown(
            f'<div class="preview">{preview_html}</div>',
            unsafe_allow_html=True,
        )

    with tab_edit:
        edited = st.text_area(
            "Edit the generated document",
            value=st.session_state.document,
            height=650,
        )
        if st.button("Save Edits", use_container_width=True):
            st.session_state.document = edited
            st.success("Edits saved for this session.")

    st.subheader("Download")
    col1, col2, col3 = st.columns(3)

    current_text = st.session_state.document
    current_type = st.session_state.generated_type or document_type

    with col1:
        st.download_button(
            "⬇️ Download TXT",
            data=format_txt(current_text),
            file_name="legalease_document.txt",
            mime="text/plain",
            use_container_width=True,
        )

    with col2:
        st.download_button(
            "⬇️ Download DOCX",
            data=format_docx(current_text, current_type, terms),
            file_name="legalease_document.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            use_container_width=True,
        )

    with col3:
        st.download_button(
            "⬇️ Download PDF",
            data=format_pdf(current_text, current_type, terms),
            file_name="legalease_document.pdf",
            mime="application/pdf",
            use_container_width=True,
        )
else:
    st.info(
        "Enter the document details in the sidebar and click "
        "**Generate Document**."
    )

st.caption(
    "LegalEase creates AI-assisted drafts. Always review important legal documents "
    "with a qualified legal professional before signing or relying on them."
)
