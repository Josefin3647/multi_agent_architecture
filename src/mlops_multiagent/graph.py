"""Definition av LangGraph-flödet."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from langgraph.graph import END, START, StateGraph

from mlops_multiagent.agents.assessment import assessment_agent
from mlops_multiagent.agents.intake_profile import intake_profile_agent
from mlops_multiagent.agents.job_matcher import job_matching_agent
from mlops_multiagent.agents.recommendation import recommendation_agent
from mlops_multiagent.models import ContactRequest
from mlops_multiagent.state import AppState
from mlops_multiagent.utils.security import validate_document_security


def security_check_node(state: AppState) -> dict[str, Any]:
    """Validerar dokument innan agentflödet får läsa innehållet."""
    file_path = Path(state["user_input"]["cv_path"])
    result = validate_document_security(file_path)

    if not result["approved"]:
        return {
            "security": result,
            "error": str(result["message"]),
        }

    return {"security": result}


def route_after_security(state: AppState) -> str:
    """Styr grafen beroende på om dokumentet godkändes."""
    security = state.get("security", {})
    if not security.get("approved", False):
        return "stop"
    return "continue"


def rejection_node(state: AppState) -> dict[str, Any]:
    """Slutnod om dokumentet inte klarar säkerhetskontrollen."""
    message = state.get("error", "Dokumentet kunde inte godkännas.")
    return {
        "final_recommendation": (
            "Flödet stoppades av säkerhetsskäl.\n"
            f"Orsak: {message}\n"
            "Ladda gärna upp ett rent och läsbart PDF- eller DOCX-dokument och försök igen."
        )
    }


def hitl_node(state: AppState) -> dict[str, Any]:
    """Enkelt HITL-steg i terminalen efter Agent 4."""
    print("\n" + "=" * 80)
    print("RESULT")
    print("=" * 80)
    print(state.get("final_recommendation", "No recommendation was generated."))

    print("\n" + "=" * 80)
    print("HITL – personal contact")
    print("=" * 80)

    answer = input("Would you like to be contacted personally? (yes/no): ").strip().lower()

    if not answer or answer == "no":
        contact = ContactRequest(wants_contact=False)
        return {
            "hitl": {
                "wants_contact": contact.wants_contact,
                "name": contact.name,
                "email": contact.email,
            }
        }

    if answer == "yes":
        name = input("Enter your name: ").strip()
        email = input("Enter your email: ").strip()
        contact = ContactRequest(wants_contact=True, name=name, email=email)
        return {
            "hitl": {
                "wants_contact": contact.wants_contact,
                "name": contact.name,
                "email": contact.email,
            }
        }

    return {
        "hitl": {
            "wants_contact": False,
            "name": "",
            "email": "",
        }
    }


def build_graph():
    """Bygger och kompilerar LangGraph-flödet."""
    graph = StateGraph(AppState)

    graph.add_node("security_check", security_check_node)
    graph.add_node("reject", rejection_node)
    graph.add_node("agent_1_intake_profile", intake_profile_agent)
    graph.add_node("agent_2_job_matching", job_matching_agent)
    graph.add_node("agent_3_assessment", assessment_agent)
    graph.add_node("agent_4_recommendation", recommendation_agent)
    graph.add_node("hitl", hitl_node)

    graph.add_edge(START, "security_check")
    graph.add_conditional_edges(
        "security_check",
        route_after_security,
        {
            "continue": "agent_1_intake_profile",
            "stop": "reject",
        },
    )
    graph.add_edge("agent_1_intake_profile", "agent_2_job_matching")
    graph.add_edge("agent_2_job_matching", "agent_3_assessment")
    graph.add_edge("agent_3_assessment", "agent_4_recommendation")
    graph.add_edge("agent_4_recommendation", "hitl")
    graph.add_edge("reject", END)
    graph.add_edge("hitl", END)

    return graph.compile()