from __future__ import annotations

from mlops_multiagent.agents.common import ensure_security_ok
from mlops_multiagent.state import FlowState
from mlops_multiagent.utils.text_processing import bool_to_swedish


def _format_top_jobs(state: FlowState) -> str:
    jobs = state.get("matched_jobs", [])[:3]
    if not jobs:
        return "Inga jobb kunde matchas direkt i den interna datakällan."

    lines: list[str] = []
    for job in jobs:
        lines.append(
            f"- {job['title']} hos {job['company']} i {job['location']} "
            f"({job['employment_type']}) – matchningspoäng {job['score']} %. {job['reasoning']}"
        )
    return "\n".join(lines)


def run_recommendation_agent(state: FlowState) -> FlowState:
    """Agent 4: Rekommendationsagent."""
    ensure_security_ok(state)

    profile = state["candidate_profile"]
    assessment = state["assessment"]

    lines = [
        "Resultat från kandidatflödet",
        "=" * 30,
        f"Önskad ort: {profile['desired_location']}",
        f"Önskad arbetstid: {profile['desired_employment_type']}",
        f"Språk: {profile.get('language') or 'ej angivet'}",
        f"Körkort: {bool_to_swedish(profile.get('driving_license'))}",
        f"Pendlingsvilja: {bool_to_swedish(profile.get('commute_willingness'))}",
        "",
    ]

    if assessment["relevant_job_count"] > 0:
        lines.extend(
            [
                f"Bedömning: {assessment['explanation']}",
                f"Antal relevanta jobb: {assessment['relevant_job_count']}",
                f"Genomsnittlig matchningsnivå: {assessment['average_match_score']} %",
                "",
            ]
        )
    else:
        lines.extend(
            [
                "Vi kunde tyvärr inte hitta några relevanta jobb just nu baserat på din profil.",
                "",
            ]
        )

    lines.extend(
        [
            "Starkaste jobbmatchningar:",
            _format_top_jobs(state),
            "",
        ]
    )

    if state.get("recurring_requirements"):
        lines.append("Återkommande krav i annonserna: " + ", ".join(state["recurring_requirements"]))
        lines.append("")

    if assessment.get("causes"):
        lines.append("Varför resultatet ser ut så här:")
        lines.extend(f"- {cause}" for cause in assessment["causes"])
        lines.append("")

    if assessment.get("skill_gaps"):
        lines.append("Identifierade kompetensgap: " + ", ".join(assessment["skill_gaps"]))
        lines.append("")

    focus = assessment.get("focus_for_agent_4")

    if focus == "jobs":
        lines.append(
            "Fokus framåt: sök jobben direkt och förbättra CV:t med tydliga exempel på dina starkaste kompetenser."
        )
    elif focus == "jobs_and_advice":
        lines.append(
            "Fokus framåt: sök de bästa jobben nu och förstärk samtidigt profilen med tydligare kompetenser och erfarenheter."
        )
    else:
        lines.append(
            "Fokus framåt: sök de få jobb som redan är rimliga och komplettera med utbildning för att öka dina chanser."
        )
        if assessment.get("suggestions"):
            lines.append("Rekommenderade utbildningar eller utvecklingsområden:")
            lines.extend(f"- {suggestion}" for suggestion in assessment["suggestions"])

    if profile.get("uncertainty_notes"):
        lines.append("")
        lines.append("Osäkerheter i tolkningen:")
        lines.extend(f"- {note}" for note in profile["uncertainty_notes"])

    state["final_response"] = "\n".join(lines)
    return state