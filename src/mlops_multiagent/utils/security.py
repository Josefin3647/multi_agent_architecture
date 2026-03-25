"""Säkerhetskontroll för inkommande dokument."""

from __future__ import annotations

from pathlib import Path

from mlops_multiagent.config import (
    ALLOWED_EXTENSIONS,
    MAX_FILE_SIZE_MB,
    MAX_TEXT_CHARS,
    SUSPICIOUS_PATTERNS,
)
from mlops_multiagent.utils.document_loader import load_document_text


def validate_file_type(file_path: Path) -> tuple[bool, str]:
    """Kontrollerar att filtypen är tillåten."""
    if file_path.suffix.lower() not in ALLOWED_EXTENSIONS:
        return False, f"Otillåten filtyp: {file_path.suffix}. Endast .pdf och .docx stöds."
    return True, "Filtypen är godkänd."


def validate_file_size(file_path: Path) -> tuple[bool, str]:
    """Kontrollerar att filstorleken är rimlig."""
    file_size_mb = file_path.stat().st_size / (1024 * 1024)
    if file_size_mb > MAX_FILE_SIZE_MB:
        return False, f"Filen är för stor ({file_size_mb:.2f} MB). Max är {MAX_FILE_SIZE_MB} MB."
    return True, "Filstorleken är godkänd."


def detect_suspicious_content(text: str) -> list[str]:
    """Letar efter enkla mönster som kan vara misstänkta i dokumentinnehållet."""
    lowered = text.lower()
    found = [pattern for pattern in SUSPICIOUS_PATTERNS if pattern in lowered]
    return found


def validate_document_security(file_path: Path) -> dict[str, object]:
    """
    Utför en enkel säkerhetskontroll:
    - filtyp
    - filstorlek
    - säker textextraktion
    - enkel upptäckt av misstänkta instruktioner
    """
    type_ok, type_msg = validate_file_type(file_path)
    if not type_ok:
        return {"approved": False, "message": type_msg, "document_text": ""}

    size_ok, size_msg = validate_file_size(file_path)
    if not size_ok:
        return {"approved": False, "message": size_msg, "document_text": ""}

    try:
        text = load_document_text(file_path)
    except Exception as exc:
        return {
            "approved": False,
            "message": f"Kunde inte läsa dokumentet säkert: {exc}",
            "document_text": "",
        }

    if not text.strip():
        return {
            "approved": False,
            "message": "Dokumentet innehåller ingen läsbar text.",
            "document_text": "",
        }

    trimmed_text = text[:MAX_TEXT_CHARS]
    suspicious = detect_suspicious_content(trimmed_text)
    if suspicious:
        return {
            "approved": False,
            "message": (
                "Dokumentet stoppades eftersom det innehåller misstänkta instruktioner "
                f"eller mönster: {', '.join(suspicious)}"
            ),
            "document_text": "",
        }

    return {
        "approved": True,
        "message": f"{type_msg} {size_msg}",
        "document_text": trimmed_text,
    }