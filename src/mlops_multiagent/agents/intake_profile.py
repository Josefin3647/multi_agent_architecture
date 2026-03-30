from __future__ import annotations

from mlops_multiagent.agents.common import ensure_security_ok
from mlops_multiagent.state import FlowState
from mlops_multiagent.utils.text_processing import (
    extract_skills_from_text,
    infer_education_level,
    split_into_candidate_experiences,
)


def run_intake_profile_agent(state: FlowState) -> FlowState:
    """Agent 1: Intake + Profilagent."""
    ensure_security_ok(state)

    extracted_text = state["security_check"]["extracted_text"]
    preferences = state["preferences"]

    skills = extract_skills_from_text(extracted_text)
    experiences = split_into_candidate_experiences(extracted_text)
    education_level = infer_education_level(extracted_text)

    uncertainty_notes: list[str] = []

    if not skills:
        uncertainty_notes.append("Inga tydliga kompetenser kunde extraheras från CV:t.")
    if education_level == "okänd":
        uncertainty_notes.append("Utbildningsnivån kunde inte identifieras säkert.")
    if len(experiences) < 2:
        uncertainty_notes.append("CV:t innehåller begränsat med tydlig erfarenhetsinformation.")

    state["candidate_profile"] = {
        "experiences": experiences,
        "skills": skills,
        "education_level": education_level,
        "desired_location": preferences["location"],
        "desired_employment_type": preferences["employment_type"],
        "language": preferences.get("language"),
        "driving_license": preferences.get("driving_license"),
        "commute_willingness": preferences.get("commute_willingness"),
        "uncertainty_notes": uncertainty_notes,
        "raw_text_preview": extracted_text[:400],
    }

    return state