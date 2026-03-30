from __future__ import annotations

from pathlib import Path

from docx import Document
from pypdf import PdfReader


class DocumentLoadError(Exception):
    """Raised when a document cannot be safely loaded."""


def extract_text_from_pdf(path: Path) -> str:
    try:
        reader = PdfReader(str(path))
        pages = [page.extract_text() or "" for page in reader.pages]
        return "\n".join(pages)
    except Exception as exc:
        raise DocumentLoadError(f"Kunde inte läsa PDF-filen: {exc}") from exc


def extract_text_from_docx(path: Path) -> str:
    try:
        document = Document(str(path))
        paragraphs = [paragraph.text for paragraph in document.paragraphs]
        return "\n".join(paragraphs)
    except Exception as exc:
        raise DocumentLoadError(f"Kunde inte läsa Word-filen: {exc}") from exc


def safe_extract_text(path: Path) -> str:
    suffix = path.suffix.lower()

    if suffix == ".pdf":
        return extract_text_from_pdf(path)
    if suffix == ".docx":
        return extract_text_from_docx(path)

    raise DocumentLoadError("Ogiltig filtyp. Endast PDF och DOCX stöds.")