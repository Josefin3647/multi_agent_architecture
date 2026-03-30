from __future__ import annotations

import re
from pathlib import Path

from mlops_multiagent.config import (
    ALLOWED_EXTENSIONS,
    MAX_FILE_SIZE_BYTES,
    SUSPICIOUS_PATTERNS,
)
from mlops_multiagent.utils.document_loader import DocumentLoadError, safe_extract_text


def validate_file_type(path: Path) -> None:
    if path.suffix.lower() not in ALLOWED_EXTENSIONS:
        raise ValueError("Ogiltig filtyp. Endast .pdf och .docx stöds.")


def validate_file_size(path: Path) -> None:
    if path.stat().st_size > MAX_FILE_SIZE_BYTES:
        raise ValueError("Filen är för stor. Max tillåten storlek är 5 MB.")


def detect_suspicious_content(text: str) -> list[str]:
    lowered = text.lower()
    matches: list[str] = []

    for pattern in SUSPICIOUS_PATTERNS:
        if re.search(pattern, lowered):
            matches.append(pattern)

    return matches


def run_security_check(cv_path: str) -> dict:
    path = Path(cv_path)

    if not path.exists():
        return {
            "is_safe": False,
            "reasons": ["Filen kunde inte hittas."],
            "extracted_text": "",
            "detected_signals": [],
        }

    try:
        validate_file_type(path)
        validate_file_size(path)

        extracted_text = safe_extract_text(path)

        reasons: list[str] = []
        if not extracted_text.strip():
            reasons.append("Dokumentet innehåller ingen läsbar text.")

        signals = detect_suspicious_content(extracted_text)
        if signals:
            reasons.append("Dokumentet innehåller misstänkta eller skadliga instruktioner.")

        return {
            "is_safe": len(reasons) == 0,
            "reasons": reasons,
            "extracted_text": extracted_text[:50000],
            "detected_signals": signals,
        }

    except (ValueError, DocumentLoadError) as exc:
        return {
            "is_safe": False,
            "reasons": [str(exc)],
            "extracted_text": "",
            "detected_signals": [],
        }
    except Exception as exc:
        return {
            "is_safe": False,
            "reasons": [f"Tekniskt fel vid säkerhetskontroll: {exc}"],
            "extracted_text": "",
            "detected_signals": [],
        }