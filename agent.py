from __future__ import annotations

from datetime import datetime, timedelta
from typing import Callable, Dict, List, Optional, Tuple, Any, TypedDict

try:
    from langgraph.graph import StateGraph, END
except ImportError as e:
    raise ImportError(
        "langgraph is required for agent graph orchestration. Install with: pip install langgraph"
    ) from e

from schemas import (
    UserProfile,
    GitHubUserExtract,
    LinkedInProfileExtract,
    HuggingFaceModelExtract,
    CareerActionRecommendation,
)
from trend_scrapping_node import process_extractions_and_recommend
from User_interaction_node import run_interaction


# Optional pluggable callbacks (override from your app before building the graph)
RUN_USER_PROCESSING_CB: Optional[
    Callable[[UserProfile], Tuple[UserProfile, Optional[GitHubUserExtract], Optional[LinkedInProfileExtract], Optional[List[HuggingFaceModelExtract]]]]
] = None


class AgentState(TypedDict, total=False):
    user: UserProfile
    github: Optional[GitHubUserExtract]
    linkedin: Optional[LinkedInProfileExtract]
    hf_models: Optional[List[HuggingFaceModelExtract]]
    recs: List[CareerActionRecommendation]
    last_user_processing_at: Optional[datetime]
    next_user_processing_at: Optional[datetime]
    schedule_interval_days: int


# --- Nodes ---

def user_processing_node(state: AgentState) -> AgentState:
    user = state["user"]
    # Invoke custom ingestion if provided; else no-op (keep previous extracts)
    if RUN_USER_PROCESSING_CB is not None:
        user, github, linkedin, hf_models = RUN_USER_PROCESSING_CB(user)
        state["user"] = user
        state["github"] = github
        state["linkedin"] = linkedin
        state["hf_models"] = hf_models

    now = datetime.now()
    state["last_user_processing_at"] = now
    interval_days = int(state.get("schedule_interval_days", 7))
    state["next_user_processing_at"] = now + timedelta(days=interval_days)
    return state


def trend_scrapping_node(state: AgentState) -> AgentState:
    user, github, linkedin, hf_models = (
        state["user"],
        state.get("github"),
        state.get("linkedin"),
        state.get("hf_models"),
    )
    aligned_user, recs = process_extractions_and_recommend(user, github=github, linkedin=linkedin, hf_models=hf_models)
    state["user"] = aligned_user
    state["recs"] = recs
    return state


def user_interaction_node(state: AgentState) -> AgentState:
    user, github, linkedin, hf_models = (
        state["user"],
        state.get("github"),
        state.get("linkedin"),
        state.get("hf_models"),
    )
    # Reuse interaction flow; it internally handles approvals/tasks
    result = run_interaction(user, github_extract=github, linkedin_extract=linkedin, hf_models=hf_models)
    state["user"] = result["updated_profile"]
    # Keep recommendations as context (could be refreshed next cycle)
    state.setdefault("recs", [])
    return state


# --- Routing helpers ---

def route_after_interaction(state: AgentState) -> str:
    """Loop in interaction until the next scheduled processing time."""
    next_at = state.get("next_user_processing_at")
    now = datetime.now()
    if next_at and now >= next_at:
        return "user_processing"
    return "user_interaction"


# --- Graph factory ---

def build_agent(user: UserProfile, schedule_interval_days: int = 7):
    """Build and compile the LangGraph app with initial state returned.

    Returns: (app, initial_state)
    """
    sg = StateGraph(AgentState)
    sg.add_node("user_processing", user_processing_node)
    sg.add_node("trend_scrapping", trend_scrapping_node)
    sg.add_node("user_interaction", user_interaction_node)

    sg.set_entry_point("user_processing")
    sg.add_edge("user_processing", "trend_scrapping")
    sg.add_edge("trend_scrapping", "user_interaction")
    sg.add_conditional_edges(
        "user_interaction",
        route_after_interaction,
        {
            "user_processing": "user_processing",
            "user_interaction": "user_interaction",
        },
    )

    app = sg.compile()
    init_state: AgentState = {
        "user": user,
        "github": None,
        "linkedin": None,
        "hf_models": None,
        "recs": [],
        "last_user_processing_at": None,
        "next_user_processing_at": datetime.now(),  # run immediately
        "schedule_interval_days": schedule_interval_days,
    }
    return app, init_state


# Optional helper to step a limited number of times (to avoid infinite loops)
def run_steps(app, state: AgentState, max_steps: int = 3):
    for _ in range(max_steps):
        state = app.invoke(state)
    return state


if __name__ == "__main__":
    # Minimal demo usage: requires a basic UserProfile
    demo = UserProfile(id=1, email="user@example.com", name="Demo User", projects=[])
    app, state = build_agent(demo, schedule_interval_days=7)
    # Run a few steps
    final = run_steps(app, state, max_steps=3)
    # Print resulting node scheduling info
    print({
        "next_user_processing_at": final.get("next_user_processing_at"),
        "last_user_processing_at": final.get("last_user_processing_at"),
    })
