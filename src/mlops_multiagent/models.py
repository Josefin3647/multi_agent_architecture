"""Datamodeller för kandidatprofil, jobbmatchning och rekommendationer."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal


EmploymentType = Literal["heltid", "deltid"]
AssessmentFocus = Literal["jobb", "jobb_och_rad", "jobb_och_utbildning"]


@dataclass
class CandidateProfile:
    """Strukturerad kandidatprofil som delas mellan agenterna."""

    raw_text: str
    experiences: list[str] = field(default_factory=list)
    skills: list[str] = field(default_factory=list)
    education_level: str = "okänd"
    desired_location: str = ""
    desired_employment_type: str = ""
    languages: list[str] = field(default_factory=list)
    has_drivers_license: bool = False
    commute_willingness: str = ""
    interpretation_uncertainty: list[str] = field(default_factory=list)


@dataclass
class JobPosting:
    """Intern representation av en jobbannons."""

    id: str
    title: str
    location: str
    employment_type: str
    required_skills: list[str]
    education_level: str
    description: str


@dataclass
class JobMatch:
    """Resultat av matchning mellan kandidatprofil och jobbannons."""

    job_id: str
    title: str
    location: str
    employment_type: str
    match_score: float
    reasons: list[str] = field(default_factory=list)
    missing_skills: list[str] = field(default_factory=list)


@dataclass
class AssessmentResult:
    """Bedömning från Agent 3."""

    strength: str
    explanation: str
    skill_gaps: list[str] = field(default_factory=list)
    education_suggestions: list[str] = field(default_factory=list)
    focus_for_agent_4: AssessmentFocus = "jobb"


@dataclass
class ContactRequest:
    """Personuppgifter som samlas in i HITL-steget."""

    wants_contact: bool
    name: str = ""
    email: str = ""