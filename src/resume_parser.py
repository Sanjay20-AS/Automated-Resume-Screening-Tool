"""Extract text from PDF, DOCX, and TXT resumes."""
from pathlib import Path

SUPPORTED_EXTENSIONS = {".pdf", ".docx", ".txt"}

def extract_text(file_path):
    path = Path(file_path)
    suffix = path.suffix.lower()
    if suffix not in SUPPORTED_EXTENSIONS:
        raise ValueError(f"Unsupported file type: {suffix}")
    if not path.exists():
        raise FileNotFoundError(path)
    if suffix == ".txt":
        return path.read_text(encoding="utf-8", errors="replace")
    if suffix == ".docx":
        from docx import Document
        doc = Document(path)
        return "\n".join(p.text for p in doc.paragraphs)
    if suffix == ".pdf":
        import pdfplumber
        pages = []
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                pages.append(page.extract_text() or "")
        return "\n".join(pages)
    return ""
