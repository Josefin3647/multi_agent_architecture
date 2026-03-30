from __future__ import annotations

from collections import Counter

from mlops_multiagent.agents.common import ensure_security_ok
from mlops_multiagent.state import FlowState


def stub_web_search_role_context(profile: dict) -> list[str]:
    skills = set(profile.get("skills", []))
    results: list[str] = []

    if {"kundservice", "butik"} & skills:
        results.extend(
            [
                "Vanliga krav i butik och kundservice är god svenska, servicevana och kassasystem.",
                "Många roller premierar säljerfarenhet, flexibilitet och grundläggande digital vana.",
            ]
        )

    if {"python", "sql", "docker", "mlops"} & skills:
        results.extend(
            [
                "Teknikroller efterfrågar ofta Python, Git, SQL, testning och moln- eller Docker-vana.",
                "Juniora tekniska roller gynnas av projektportfölj och tydligt beskriven systemvana.",
            ]
        )

    if not results:
        results.extend(
            [
                "Vanliga generella krav är tydlig kommunikation, digital vana och relevant arbetslivserfarenhet.",
                "Kompletterande kortkurser kan stärka en profil när antalet matchande jobb är lågt.",
            ]
        )

    return results


def stub_training_suggestions(skill_gaps: list[str]) -> list[str]:
    mapping = {
        "truckkort": "Truckutbildning A/B",
        "administration": "Grundkurs i administration och digitala kontorsverktyg",
        "excel": "Excel grund till fortsättning",
        "crm": "Introduktion till CRM-system och kundhantering",
        "git": "Git och versionshantering för nybörjare",
        "sql": "SQL-grunder för data och rapportering",
        "docker": "Docker introduktion",
        "api": "Grundkurs i API:er och integrationer",
    }

    suggestions = [mapping[gap] for gap in skill_gaps if gap in mapping]
    return sorted(set(suggestions)) or ["Kort yrkesanpassad kurs inom det område du vill söka jobb i"]


def run_assessment_agent(state: FlowState) -> FlowState:
    """Agent 3: Bedömningsagent."""
    ensure_security_ok(state)

    profile = state["candidate_profile"]
    matched_jobs = state.get("matched_jobs", [])

    average_score = round(
        sum(job["score"] for job in matched_jobs) / max(len(matched_jobs), 1),
        1,
    )
    relevant_count = len([job for job in matched_jobs if job["score"] >= 45])

    all_required_skills: list[str] = []
    for job in matched_jobs:
        all_required_skills.extend(job["required_skills"])

    required_counter = Counter(all_required_skills)
    profile_skills = set(profile.get("skills", []))
    skill_gaps = [skill for skill, _ in required_counter.most_common() if skill not in profile_skills][:5]

    causes: list[str] = []

    if relevant_count < 3:
        causes.append("Det finns få relevanta jobb i den interna datakällan för vald profil.")
    if average_score < 50:
        causes.append("Matchningsnivån är överlag låg jämfört med krav i annonserna.")
    if state["preferences"].get("employment_type") == "deltid":
        causes.append("Önskemål om deltid minskar urvalet av jobb.")
    if not profile.get("skills"):
        causes.append("CV:t är otydligt eller innehåller för få tydliga kompetenser.")
    if state["preferences"].get("location") and len(matched_jobs) <= 2:
        causes.append("Geografisk begränsning påverkar sannolikt antalet träffar.")

    if relevant_count > 8 and average_score >= 65:
        strength = "strong"
        focus = "jobs"
        explanation = "Matchningen är stark. Det finns flera relevanta jobb med god överensstämmelse mot profilen."
    elif 3 <= relevant_count <= 7:
        strength = "medium"
        focus = "jobs_and_advice"
        explanation = "Matchningen är användbar men inte helt stark. Jobb bör kombineras med mindre kompetensråd."
    else:
        strength = "weak"
        focus = "jobs_and_training"
        explanation = "Matchningen är svag eller begränsad. Resultatet bör kompletteras med utbildningsförslag."

    market_context = stub_web_search_role_context(profile)
    suggestions = stub_training_suggestions(skill_gaps) if focus == "jobs_and_training" else []

    state["assessment"] = {
        "strength": strength,
        "explanation": explanation,
        "average_match_score": average_score,
        "relevant_job_count": relevant_count,
        "skill_gaps": skill_gaps,
        "causes": causes,
        "suggestions": suggestions,
        "focus_for_agent_4": focus,
        "market_context": market_context,
    }

    return state