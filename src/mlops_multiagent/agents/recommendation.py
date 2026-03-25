"""Agent 4: Rekommendationsagent."""

from __future__ import annotations

from mlops_multiagent.state import AppState
from mlops_multiagent.utils.text_processing import format_bullets


def recommendation_agent(state: AppState) -> dict[str, str]:
    """Sammanställer slutresultatet på ett tydligt och användbart sätt."""
    profile = state["candidate_profile"]
    jobs = state.get("job_matches", [])
    assessment = state["assessment"]

    top_jobs = jobs[:3]
    location = profile["desired_location"]
    focus = assessment["focus_for_agent_4"]

    lines: list[str] = []
    lines.append(
        f"Du har just nu {len(jobs)} jobb som matchar din profil i eller nära {location}."
    )

    if top_jobs:
        lines.append("\nDina starkaste matchningar är:")
        for job in top_jobs:
            reason = "; ".join(job["reasons"][:2]) if job["reasons"] else "Grundmatchning mot profil"
            lines.append(
                f"- {job['title']} ({job['employment_type']}, {job['location']}) "
                f"– matchningspoäng {job['match_score']}. Varför: {reason}."
            )
    else:
        lines.append("\nInga tydliga toppjobb kunde identifieras i den interna jobbdatakällan.")

    lines.append(f"\nBedömning: {assessment['explanation']}")

    if focus == "jobb":
        lines.append(
            "\nFokus bör främst ligga på att söka jobb nu. "
            "Mindre förbättringar i CV:t kan vara att göra kompetenser och erfarenheter ännu tydligare."
        )
    elif focus == "jobb_och_rad":
        lines.append(
            "\nDet finns relevanta jobb, men du kan öka dina chanser genom att förstärka några återkommande kompetenser."
        )
        if assessment["skill_gaps"]:
            lines.append("\nKompetenser som ofta återkommer i annonserna:")
            lines.append(format_bullets(assessment["skill_gaps"]))
    else:
        lines.append(
            "\nUrvalet är begränsat. Det är därför bra att både titta på de jobb som finns nu "
            "och samtidigt stärka profilen med kortare utbildningar eller kurser."
        )
        if assessment["skill_gaps"]:
            lines.append("\nIdentifierade kompetensgap:")
            lines.append(format_bullets(assessment["skill_gaps"]))
        if assessment["education_suggestions"]:
            lines.append("\nFörslag på utvecklingsområden eller utbildningar:")
            lines.append(format_bullets(assessment["education_suggestions"]))

    return {"final_recommendation": "\n".join(lines)}