"""Data models for candidate profile, job matching, and recommendations."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal


EmploymentType = Literal["full-time", "part-time"]
AssessmentFocus = Literal["job", "job_and_advice", "job_and_education"]


@dataclass
class CandidateProfile:
    """Structured candidate profile shared between agents."""

    raw_text: str
    experiences: list[str] = field(default_factory=list)
    skills: list[str] = field(default_factory=list)
    education_level: str = "unknown"
    desired_location: str = ""
    desired_employment_type: str = ""
    languages: list[str] = field(default_factory=list)
    has_drivers_license: bool = False
    commute_willingness: str = ""
    interpretation_uncertainty: list[str] = field(default_factory=list)


@dataclass
class JobPosting:
    """Internal representation of a job posting."""

    id: str
    title: str
    location: str
    employment_type: str
    required_skills: list[str]
    education_level: str
    description: str


@dataclass
class JobMatch:
    """Result of matching between candidate profile and job posting."""

    job_id: str
    title: str
    location: str
    employment_type: str
    match_score: float
    reasons: list[str] = field(default_factory=list)
    missing_skills: list[str] = field(default_factory=list)


@dataclass
class AssessmentResult:
    """Assessment from Agent 3."""

    strength: str
    explanation: str
    skill_gaps: list[str] = field(default_factory=list)
    education_suggestions: list[str] = field(default_factory=list)
    focus_for_agent_4: AssessmentFocus = "job"


@dataclass
class ContactRequest:
    """Personal details collected during the HITL step."""

    wants_contact: bool
    name: str = ""
    email: str = ""