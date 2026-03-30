from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path
from typing import Any

SKILL_KEYWORDS = [
    "python",
    "sql",
    "excel",
    "kundservice",
    "butik",
    "försäljning",
    "administration",
    "office",
    "microsoft office",
    "kommunikation",
    "truckkort",
    "lager",
    "java",
    "c#",
    "machine learning",
    "mlops",
    "docker",
    "git",
    "pandas",
    "api",
    "support",
    "crm",
    "svenska",
    "engelska",
]

EDUCATION_HINTS = {
    "gymnasium": ["gymnasium", "gymnasie", "high school"],
    "yrkeshögskola": ["yrkeshögskola", "yh", "vocational"],
    "kandidat": ["kandidat", "bachelor"],
    "master": ["master", "magister"],
}


def normalize_text(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip().lower())


def extract_skills_from_text(text: str) -> list[str]:
    lowered = normalize_text(text)
    found = [skill for skill in SKILL_KEYWORDS if skill in lowered]
    return sorted(set(found))


def infer_education_level(text: str) -> str:
    lowered = normalize_text(text)
    for level, hints in EDUCATION_HINTS.items():
        if any(hint in lowered for hint in hints):
            return level
    return "okänd"


def split_into_candidate_experiences(text: str) -> list[str]:
    chunks = re.split(r"[\n\r]+|•|- ", text)
    cleaned = [chunk.strip() for chunk in chunks if len(chunk.strip()) > 20]
    return cleaned[:8]


def load_jobs(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def compute_job_match(profile: dict, job: dict) -> dict:
    profile_skills = set(profile.get("skills", []))
    required = set(normalize_text(skill) for skill in job["required_skills"])
    preferred = set(normalize_text(skill) for skill in job["preferred_skills"])

    matched_required = required & profile_skills
    matched_preferred = preferred & profile_skills

    required_score = len(matched_required) / max(len(required), 1)
    preferred_score = len(matched_preferred) / max(len(preferred), 1)
    score = round((required_score * 0.75 + preferred_score * 0.25) * 100, 1)

    reasons: list[str] = []
    if matched_required:
        reasons.append(f"Matchar centrala krav: {', '.join(sorted(matched_required))}")
    if matched_preferred:
        reasons.append(f"Matchar meriterande krav: {', '.join(sorted(matched_preferred))}")
    if not reasons:
        reasons.append("Begränsad direkt matchning mot kravprofilen")

    return {
        "id": job["id"],
        "title": job["title"],
        "company": job["company"],
        "location": job["location"],
        "employment_type": job["employment_type"],
        "required_skills": job["required_skills"],
        "preferred_skills": job["preferred_skills"],
        "score": score,
        "reasoning": "; ".join(reasons),
    }


def recurring_requirements(matched_jobs: list[dict]) -> list[str]:
    counter: Counter[str] = Counter()
    for job in matched_jobs:
        counter.update([*job["required_skills"], *job["preferred_skills"]])
    return [item for item, _ in counter.most_common(5)]


def bool_to_swedish(value: bool | None) -> str:
    if value is True:
        return "ja"
    if value is False:
        return "nej"
    return "ej angivet"