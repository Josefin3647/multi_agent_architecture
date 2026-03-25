"""Agent 3: Bedömningsagent."""

from __future__ import annotations

from statistics import mean
from typing import Any

from mlops_multiagent.models import AssessmentResult
from mlops_multiagent.state import AppState


def stub_web_search(query: str) -> list[dict[str, str]]:
    """
    Stubbad webbsökning.

    I en riktig lösning hade detta kunnat anropa ett webbsöksverktyg.
    Här returneras hårdkodade resultat för att visa arkitekturen.
    """
    knowledge_base = {
        "kundservice": [
            {
                "title": "Vanliga krav inom kundservice",
                "snippet": "Svenska, serviceförmåga, administration och digital vana återkommer ofta.",
            }
        ],
        "butik": [
            {
                "title": "Vanliga krav inom butik",
                "snippet": "Kassa, kundbemötande, försäljning och ibland truckkort eller varuplock.",
            }
        ],
        "administration": [
            {
                "title": "Efterfrågade administrativa kompetenser",
                "snippet": "Excel, dokumenthantering och digitala kontorsverktyg är vanliga krav.",
            }
        ],
        "truckkort": [
            {
                "title": "Rekommenderad utbildning",
                "snippet": "Kort truckutbildning kan stärka möjligheten för lager- och logistikjobb.",
            }
        ],
    }

    results: list[dict[str, str]] = []
    query_lower = query.lower()
    for key, items in knowledge_base.items():
        if key in query_lower:
            results.extend(items)

    if not results:
        results.append(
            {
                "title": "Allmän arbetsmarknadskontext",
                "snippet": "Digital vana, språk och tydligt formulerade kompetenser förbättrar ofta matchning.",
            }
        )
    return results


def _identify_primary_reason(
    profile: dict[str, Any],
    job_matches: list[dict[str, Any]],
    recurring_requirements: list[str],
) -> str:
    """Förklarar varför matchningen blev stark eller svag."""
    if not job_matches:
        return "Det finns få eller inga träffar i den interna datakällan för den här kombinationen av profil och önskemål."

    desired_location = str(profile["desired_location"]).lower()
    desired_type = str(profile["desired_employment_type"]).lower()

    same_location = [job for job in job_matches if job["location"].lower() == desired_location]
    same_type = [job for job in job_matches if job["employment_type"].lower() == desired_type]

    if len(same_location) < max(1, len(job_matches) // 2):
        return "Geografisk begränsning verkar minska urvalet."
    if len(same_type) < max(1, len(job_matches) // 2):
        return "Önskemål om arbetstid verkar minska urvalet."
    if recurring_requirements:
        return "Kompetensgap påverkar sannolikt matchningen."
    if profile.get("interpretation_uncertainty"):
        return "CV:t eller profilen verkar något otydlig, vilket kan försvåra matchning."
    return "Matchningen påverkas troligen av allmän efterfrågan i området och kandidatens profil."


def assessment_agent(state: AppState) -> dict[str, Any]:
    """Avgör om resultatet främst ska fokusera på jobb eller även råd/utbildning."""
    profile = state["candidate_profile"]
    job_matches = state.get("job_matches", [])
    recurring_requirements = state.get("recurring_requirements", [])

    num_jobs = len(job_matches)
    avg_score = mean([job["match_score"] for job in job_matches]) if job_matches else 0.0

    skill_gaps = recurring_requirements[:5]
    explanation_root = _identify_primary_reason(profile, job_matches, recurring_requirements)

    search_queries = [
        "kundservice butik administration efterfrågade kompetenser",
        "truckkort utbildning",
    ]
    web_context: list[str] = []
    for query in search_queries:
        for item in stub_web_search(query):
            web_context.append(item["snippet"])

    education_suggestions: list[str] = []
    if "truckkort" in skill_gaps:
        education_suggestions.append("Truckutbildning")
    if any(skill in skill_gaps for skill in ["administration", "excel", "digitala kontorsverktyg"]):
        education_suggestions.append("Grundkurs i administration och digitala kontorsverktyg")
    if "engelska" in skill_gaps:
        education_suggestions.append("Praktisk yrkesengelska")
    if "it-support" in skill_gaps:
        education_suggestions.append("Introduktion till IT-support och ärendehantering")

    education_suggestions = list(dict.fromkeys(education_suggestions))

    if num_jobs > 8 and avg_score >= 60:
        focus = "jobb"
        strength = "stark"
    elif 3 <= num_jobs <= 7:
        focus = "jobb_och_rad"
        strength = "medel"
    else:
        focus = "jobb_och_utbildning"
        strength = "svag"

    explanation = (
        f"Antal relevanta jobb: {num_jobs}. Genomsnittlig matchning: {avg_score:.1f}. "
        f"Bedömning: {explanation_root} "
        f"Kompletterande marknadskontext: {' '.join(web_context[:2])}"
    )

    result = AssessmentResult(
        strength=strength,
        explanation=explanation,
        skill_gaps=skill_gaps,
        education_suggestions=education_suggestions,
        focus_for_agent_4=focus,
    )

    return {
        "assessment": {
            "strength": result.strength,
            "explanation": result.explanation,
            "skill_gaps": result.skill_gaps,
            "education_suggestions": result.education_suggestions,
            "focus_for_agent_4": result.focus_for_agent_4,
        }
    }