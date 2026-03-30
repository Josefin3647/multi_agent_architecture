from __future__ import annotations

from mlops_multiagent.agents.common import ensure_security_ok
from mlops_multiagent.config import JOBS_FILE
from mlops_multiagent.state import FlowState
from mlops_multiagent.utils.text_processing import (
    compute_job_match,
    load_jobs,
    recurring_requirements,
)


def run_job_matcher_agent(state: FlowState) -> FlowState:
    """Agent 2: Jobbmatchningsagent."""
    ensure_security_ok(state)

    profile = state["candidate_profile"]
    all_jobs = load_jobs(JOBS_FILE)

    filtered_jobs: list[dict] = []
    desired_location = profile["desired_location"].lower()
    desired_employment_type = profile["desired_employment_type"].lower()
    commute_ok = bool(profile.get("commute_willingness"))

    for job in all_jobs:
        same_location = job["location"].lower() == desired_location
        same_employment_type = job["employment_type"].lower() == desired_employment_type

        if (same_location or commute_ok) and same_employment_type:
            filtered_jobs.append(job)

    matches = [compute_job_match(profile, job) for job in filtered_jobs]
    matches = sorted(matches, key=lambda item: item["score"], reverse=True)

    state["matched_jobs"] = matches[:10]
    state["recurring_requirements"] = recurring_requirements(matches[:10])

    return state