"""Säker och enkel inläsning av PDF- och DOCX-filer."""

from __future__ import annotations

from pathlib import Path

from docx import Document
from pypdf import PdfReader


def read_pdf_text(file_path: Path) -> str:
    """Läser text från PDF med pypdf."""
    reader = PdfReader(str(file_path))
    text_parts: list[str] = []

    for page in reader.pages:
        page_text = page.extract_text() or ""
        text_parts.append(page_text)

    return "\n".join(text_parts).strip()


def read_docx_text(file_path: Path) -> str:
    """Läser text från DOCX med python-docx."""
    document = Document(str(file_path))
    paragraphs = [paragraph.text for paragraph in document.paragraphs if paragraph.text.strip()]
    return "\n".join(paragraphs).strip()


def load_document_text(file_path: Path) -> str:
    """Väljer rätt loader beroende på filändelse."""
    suffix = file_path.suffix.lower()

    if suffix == ".pdf":
        return read_pdf_text(file_path)
    if suffix == ".docx":
        return read_docx_text(file_path)

    raise ValueError(f"Filtypen {suffix} stöds inte.")