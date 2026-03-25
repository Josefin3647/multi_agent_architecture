"""Agent 1: Intake + Profilagent."""

from __future__ import annotations

from typing import Any

from mlops_multiagent.models import CandidateProfile
from mlops_multiagent.state import AppState
from mlops_multiagent.utils.text_processing import (
    extract_experiences,
    extract_skills,
    infer_education_level,
)


def _normalize_optional_list(raw_value: str) -> list[str]:
    """Delar upp en kommaseparerad sträng till en normaliserad lista."""
    if not raw_value.strip():
        return []
    return sorted({item.strip().lower() for item in raw_value.split(",") if item.strip()})


def intake_profile_agent(state: AppState) -> dict[str, Any]:
    """Skapar en strukturerad kandidatprofil från användarinput och CV-text."""
    user_input = state["user_input"]
    security = state["security"]
    cv_text = str(security.get("document_text", ""))

    skills = extract_skills(cv_text)
    experiences = extract_experiences(cv_text)
    education_level = infer_education_level(cv_text)

    uncertainties: list[str] = []
    if not skills:
        uncertainties.append("Inga tydliga kompetenser kunde extraheras från CV:t.")
    if education_level == "okänd":
        uncertainties.append("Utbildningsnivån kunde inte avgöras tydligt.")
    if not experiences:
        uncertainties.append("Yrkeserfarenheter kunde inte extraheras tydligt.")

    profile = CandidateProfile(
        raw_text=cv_text,
        experiences=experiences,
        skills=skills,
        education_level=education_level,
        desired_location=str(user_input["location"]).strip(),
        desired_employment_type=str(user_input["employment_type"]).strip().lower(),
        languages=_normalize_optional_list(str(user_input.get("languages", ""))),
        has_drivers_license=bool(user_input.get("drivers_license", False)),
        commute_willingness=str(user_input.get("commute_willingness", "")).strip().lower(),
        interpretation_uncertainty=uncertainties,
    )

    return {
        "candidate_profile": {
            "raw_text": profile.raw_text,
            "experiences": profile.experiences,
            "skills": profile.skills,
            "education_level": profile.education_level,
            "desired_location": profile.desired_location,
            "desired_employment_type": profile.desired_employment_type,
            "languages": profile.languages,
            "has_drivers_license": profile.has_drivers_license,
            "commute_willingness": profile.commute_willingness,
            "interpretation_uncertainty": profile.interpretation_uncertainty,
        }
    }