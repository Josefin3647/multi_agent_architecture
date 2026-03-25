"""Hjälpfunktioner för enkel text- och kompetensanalys."""

from __future__ import annotations

import re
from collections import Counter


KNOWN_SKILLS = {
    "kundservice",
    "försäljning",
    "kassa",
    "administration",
    "excel",
    "digitala kontorsverktyg",
    "telefonvana",
    "svenska",
    "engelska",
    "lager",
    "truckkort",
    "omsorg",
    "journalföring",
    "skrivande",
    "cms",
    "digitala verktyg",
    "it-support",
    "felsökning",
    "varuplock",
}


def normalize_text(text: str) -> str:
    """Normaliserar text för enklare jämförelser."""
    text = text.lower().strip()
    text = re.sub(r"\s+", " ", text)
    return text


def tokenize(text: str) -> list[str]:
    """Tokeniserar text på ett enkelt sätt."""
    cleaned = re.sub(r"[^a-zA-ZåäöÅÄÖ0-9\s-]", " ", text.lower())
    return [token for token in cleaned.split() if token]


def extract_skills(text: str) -> list[str]:
    """Extraherar kända kompetenser via enkel nyckelordsdetektion."""
    norm = normalize_text(text)
    found = [skill for skill in KNOWN_SKILLS if skill in norm]
    return sorted(set(found))


def infer_education_level(text: str) -> str:
    """Gissar utbildningsnivå från CV-text."""
    norm = normalize_text(text)

    if any(term in norm for term in ["universitet", "kandidatexamen", "master", "högskola"]):
        return "eftergymnasial"
    if any(term in norm for term in ["yrkesutbildning", "yhutbildning", "yh", "komvux vård"]):
        return "yrkesutbildning"
    if any(term in norm for term in ["gymnasieexamen", "gymnasium", "handel och administration"]):
        return "gymnasium"
    return "okänd"


def extract_experiences(text: str) -> list[str]:
    """Extraherar förenklade erfarenheter genom rader med vanliga jobbord."""
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    keywords = (
        "butik",
        "kund",
        "kundtjänst",
        "sälj",
        "lager",
        "reception",
        "support",
        "administrat",
        "undersköterska",
        "redaktör",
    )
    experiences: list[str] = []
    for line in lines:
        lower = line.lower()
        if any(keyword in lower for keyword in keywords):
            experiences.append(line)
    return experiences[:10]


def most_common_items(values: list[str], top_k: int = 5) -> list[str]:
    """Returnerar de vanligaste elementen i en lista."""
    counter = Counter(values)
    return [item for item, _ in counter.most_common(top_k)]


def format_bullets(items: list[str]) -> str:
    """Formaterar en lista som punktlista."""
    if not items:
        return "- Inga"
    return "\n".join(f"- {item}" for item in items)