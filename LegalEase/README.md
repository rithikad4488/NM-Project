# LegalEase — AI-Powered Legal Document Generator

LegalEase is a local full-stack application based on the supplied project documentation.

## Architecture

- Frontend: Streamlit
- Backend: FastAPI + Uvicorn
- AI: Google Gemini
- Document generation: python-docx + fpdf2
- Configuration: `.env`
- API: `POST /generate`
- Exports: TXT, DOCX, PDF
- Tests: pytest

The application follows the supplied workflow: document type, parties, terms, effective date -> Gemini generation -> editable preview -> export.

> Legal disclaimer: AI-generated content is for drafting/informational purposes and is not a substitute for advice from a qualified lawyer.

## 1. Requirements

- Windows 10/11
- Python 3.10 or newer
- Internet connection for Gemini generation
- A Google Gemini API key

## 2. VS Code setup

Open this folder in VS Code.

Open **Terminal > New Terminal**, then run:

```powershell
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and put your API key in it:

```text
GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=gemini-1.5-pro
BACKEND_URL=http://127.0.0.1:8000
```

If your Google account does not provide `gemini-1.5-pro`, change `GEMINI_MODEL` to a model available to your API account.

## 3. Run the backend

Terminal 1:

```powershell
.venv\Scripts\activate
uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

Open:

- http://127.0.0.1:8000
- http://127.0.0.1:8000/docs

You should see the LegalEase health response.

## 4. Run the frontend

Terminal 2:

```powershell
.venv\Scripts\activate
streamlit run frontend/app.py
```

Streamlit normally opens:

http://localhost:8501

## 5. Test the application

1. Select or enter a document type.
2. Enter parties.
3. Enter terms separated by semicolons.
4. Enter an effective date.
5. Click **Generate Document**.
6. Review the preview.
7. Click **Edit Document** if changes are required.
8. Download TXT, DOCX or PDF.

## 6. Test the API directly

With the backend running:

```powershell
python -m pytest -q
```

The API can also be tested in Swagger at:

http://127.0.0.1:8000/docs

Example JSON:

```json
{
  "document_type": "Non-Disclosure Agreement",
  "parties": "Jane Doe (Disclosing Party), TechNova Inc. (Receiving Party)",
  "terms": "Confidential information must be protected; Disclosure is limited to authorized personnel; Agreement may be terminated with 15 days notice",
  "effective_date": "2026-10-07"
}
```

## 7. Project structure

```text
LegalEase/
├── backend/
│   ├── __init__.py
│   ├── main.py
│   ├── routes.py
│   └── schemas.py
├── ai_core/
│   ├── __init__.py
│   └── gemini_generator.py
├── document_utils/
│   ├── __init__.py
│   ├── common.py
│   ├── docx_formatter.py
│   ├── pdf_formatter.py
│   └── txt_formatter.py
├── frontend/
│   └── app.py
├── tests/
│   ├── __init__.py
│   ├── test_health.py
│   └── test_formatters.py
├── assets/
│   └── README.txt
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Troubleshooting

### `python is not recognized`
Install Python from python.org and enable **Add Python to PATH** during installation.

### PowerShell blocks activation
Use:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then activate again.

### Gemini error
Check `.env`, API key, internet connection, and `GEMINI_MODEL`. The app returns a readable error instead of crashing.

### DOCX/PDF logo
A logo is optional. Place a PNG/JPG logo at `assets/logo.png`. The DOCX/PDF exporters automatically use it when present.

### Port already in use
Use another backend port:

```powershell
uvicorn backend.main:app --reload --port 8001
```

Then set:

```text
BACKEND_URL=http://127.0.0.1:8001
```

in `.env`.

## Security

- Never commit `.env`.
- Never put the Gemini API key in Streamlit source code.
- Do not use real confidential legal information during development/testing.
- For production, add authentication, HTTPS, database storage, audit logging and stronger privacy controls.
