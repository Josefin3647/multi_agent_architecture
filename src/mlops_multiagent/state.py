"""Shared state för LangGraph-flödet."""

from __future__ import annotations

from typing import Any, TypedDict


class AppState(TypedDict, total=False):
    """Delad state som skickas mellan noderna i grafen."""

    user_input: dict[str, Any]
    security: dict[str, Any]
    candidate_profile: dict[str, Any]
    job_matches: list[dict[str, Any]]
    recurring_requirements: list[str]
    assessment: dict[str, Any]
    final_recommendation: str
    hitl: dict[str, Any]
    error: str