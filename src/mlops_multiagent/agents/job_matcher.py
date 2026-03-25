"""Agent 2: Jobbmatchningsagent."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

from mlops_multiagent.config import DEFAULT_JOBS_PATH
from mlops_multiagent.models import JobMatch, JobPosting
from mlops_multiagent.state import AppState


def load_job_postings(path: Path = DEFAULT_JOBS_PATH) -> list[JobPosting]:
    """Läser jobbannonser från lokal JSON."""
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    jobs = [
        JobPosting(
            id=item["id"],
            title=item["title"],
            location=item["location"],
            employment_type=item["employment_type"],
            required_skills=item["required_skills"],
            education_level=item["education_level"],
            description=item["description"],
        )
        for item in data
    ]
    return jobs


def _education_rank(level: str) -> int:
    """Grov rangordning av utbildningsnivå."""
    ranks = {
        "okänd": 0,
        "gymnasium": 1,
        "yrkesutbildning": 2,
        "eftergymnasial": 3,
    }
    return ranks.get(level.lower(), 0)


def _score_job(profile: dict[str, Any], job: JobPosting) -> JobMatch:
    """Beräknar en enkel matchningspoäng och motivering."""
    desired_location = str(profile["desired_location"]).lower()
    desired_type = str(profile["desired_employment_type"]).lower()
    candidate_skills = {skill.lower() for skill in profile["skills"]}
    job_skills = {skill.lower() for skill in job.required_skills}

    score = 0.0
    reasons: list[str] = []

    skill_overlap = sorted(candidate_skills.intersection(job_skills))
    missing_skills = sorted(job_skills.difference(candidate_skills))

    if job.location.lower() == desired_location:
        score += 35
        reasons.append("Rätt arbetsort")
    elif profile.get("commute_willingness"):
        score += 10
        reasons.append("Annonsen ligger utanför önskad ort men pendlingsvilja finns")

    if job.employment_type.lower() == desired_type:
        score += 25
        reasons.append("Rätt arbetstid")
    else:
        score -= 10

    if job_skills:
        skill_score = (len(skill_overlap) / len(job_skills)) * 30
        score += skill_score

    if skill_overlap:
        reasons.append(f"Matchande kompetenser: {', '.join(skill_overlap[:4])}")

    if _education_rank(profile["education_level"]) >= _education_rank(job.education_level):
        score += 10
        reasons.append("Utbildningsnivån verkar tillräcklig")

    if "körkort" in job_skills and profile.get("has_drivers_license"):
        score += 5
        reasons.append("Körkort matchar annonskrav")

    score = max(0.0, min(100.0, round(score, 1)))

    return JobMatch(
        job_id=job.id,
        title=job.title,
        location=job.location,
        employment_type=job.employment_type,
        match_score=score,
        reasons=reasons,
        missing_skills=missing_skills,
    )


def job_matching_agent(state: AppState) -> dict[str, Any]:
    """Matchar kandidatprofilen mot intern jobbdatakälla."""
    profile = state["candidate_profile"]
    jobs = load_job_postings()

    scored_matches = [_score_job(profile, job) for job in jobs]

    scored_matches.sort(key=lambda match: match.match_score, reverse=True)
    top_matches = [match for match in scored_matches if match.match_score >= 20][:10]

    recurring_counter: Counter[str] = Counter()
    for match in top_matches:
        for missing_skill in match.missing_skills:
            recurring_counter[missing_skill] += 1

    recurring_requirements = [skill for skill, _ in recurring_counter.most_common(5)]

    return {
        "job_matches": [
            {
                "job_id": match.job_id,
                "title": match.title,
                "location": match.location,
                "employment_type": match.employment_type,
                "match_score": match.match_score,
                "reasons": match.reasons,
                "missing_skills": match.missing_skills,
            }
            for match in top_matches
        ],
        "recurring_requirements": recurring_requirements,
    }