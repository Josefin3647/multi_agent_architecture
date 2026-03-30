from __future__ import annotations

from typing import Any, Literal, TypedDict


class CandidatePreferences(TypedDict, total=False):
    location: str
    employment_type: Literal["heltid", "deltid"]
    language: str | None
    driving_license: bool | None
    commute_willingness: bool | None


class SecurityCheckResult(TypedDict):
    is_safe: bool
    reasons: list[str]
    extracted_text: str
    detected_signals: list[str]


class CandidateProfile(TypedDict, total=False):
    experiences: list[str]
    skills: list[str]
    education_level: str
    desired_location: str
    desired_employment_type: str
    language: str | None
    driving_license: bool | None
    commute_willingness: bool | None
    uncertainty_notes: list[str]
    raw_text_preview: str


class JobMatch(TypedDict):
    id: str
    title: str
    company: str
    location: str
    employment_type: str
    required_skills: list[str]
    preferred_skills: list[str]
    score: float
    reasoning: str


class AssessmentResult(TypedDict, total=False):
    strength: Literal["strong", "medium", "weak"]
    explanation: str
    average_match_score: float
    relevant_job_count: int
    skill_gaps: list[str]
    causes: list[str]
    suggestions: list[str]
    focus_for_agent_4: Literal["jobs", "jobs_and_advice", "jobs_and_training"]
    market_context: list[str]


class FlowState(TypedDict, total=False):
    cv_path: str
    preferences: CandidatePreferences
    security_check: SecurityCheckResult
    candidate_profile: CandidateProfile
    matched_jobs: list[JobMatch]
    recurring_requirements: list[str]
    assessment: AssessmentResult
    final_response: str
    stop_flow: bool
    error_message: str | None
    contact_request: dict[str, str] | None
    debug: dict[str, Any]