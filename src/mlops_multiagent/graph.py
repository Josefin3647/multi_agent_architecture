from __future__ import annotations

from langgraph.graph import END, START, StateGraph

from mlops_multiagent.agents.assessment import run_assessment_agent
from mlops_multiagent.agents.intake_profile import run_intake_profile_agent
from mlops_multiagent.agents.job_matcher import run_job_matcher_agent
from mlops_multiagent.agents.recommendation import run_recommendation_agent
from mlops_multiagent.state import FlowState
from mlops_multiagent.utils.security import run_security_check


def security_node(state: FlowState) -> FlowState:
    result = run_security_check(state["cv_path"])
    state["security_check"] = result

    if not result["is_safe"]:
        state["stop_flow"] = True
        state["error_message"] = (
            "CV:t kunde inte behandlas eftersom säkerhetskontrollen stoppade flödet. "
            + " ".join(result["reasons"])
        )

    return state


def blocked_node(state: FlowState) -> FlowState:
    return state


def route_after_security(state: FlowState) -> str:
    return "blocked" if state.get("stop_flow") else "agent_1"


def build_graph():
    workflow = StateGraph(FlowState)

    workflow.add_node("security", security_node)
    workflow.add_node("blocked", blocked_node)
    workflow.add_node("agent_1", run_intake_profile_agent)
    workflow.add_node("agent_2", run_job_matcher_agent)
    workflow.add_node("agent_3", run_assessment_agent)
    workflow.add_node("agent_4", run_recommendation_agent)

    workflow.add_edge(START, "security")
    workflow.add_conditional_edges(
        "security",
        route_after_security,
        {
            "blocked": "blocked",
            "agent_1": "agent_1",
        },
    )
    workflow.add_edge("blocked", END)
    workflow.add_edge("agent_1", "agent_2")
    workflow.add_edge("agent_2", "agent_3")
    workflow.add_edge("agent_3", "agent_4")
    workflow.add_edge("agent_4", END)

    return workflow.compile()