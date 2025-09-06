from typing import List, Optional, Callable, Dict, Any, Tuple
from pydantic import BaseModel, Field

from schemas import (
	UserProfile,
	Skills,
	Projects,
	CareerActionRecommendation,
)
from trend_scrapping_node import (
	process_extractions_and_recommend,
	align_extractions_with_profile,
)


class ApprovalDecision(str):
	APPROVED = "Approved"
	DEFERRED = "Deferred"
	REJECTED = "Rejected"


class ValidationTask(BaseModel):
	title: str
	description: str
	related_skill: Optional[str] = None
	expected_outcome: Optional[str] = None
	difficulty: str = Field(default="Medium")


class InteractionEvent(BaseModel):
	event_type: str
	message: str
	payload: Dict[str, Any] = Field(default_factory=dict)


def _missing_profile_fields(user: UserProfile) -> List[str]:
	missing = []
	if not user.location:
		missing.append("location")
	if not user.skills:
		missing.append("skills")
	if not user.projects:
		missing.append("projects")
	if not user.certifications:
		missing.append("certifications")
	if not user.blogs:
		missing.append("blogs")
	return missing


def generate_personalized_questions(user: UserProfile) -> List[str]:
	questions: List[str] = []
	for field in _missing_profile_fields(user):
		if field == "location":
			questions.append("What's your current city and country?")
		elif field == "skills":
			questions.append("List your top 5 skills with self-rated strength (Beginner/Intermediate/Advanced).")
		elif field == "projects":
			questions.append("Share 2–3 recent projects (title, one-line description, tech used, link).")
		elif field == "certifications":
			questions.append("Do you have any certifications? Provide title, issuer, and date.")
		elif field == "blogs":
			questions.append("Have you written any blogs or posts? Provide title, link, and brief summary.")

	# Add enrichment questions even if fields exist
	questions.append("Which roles are you targeting in the next 6 months (e.g., Data Engineer, ML Engineer)?")
	questions.append("What industries interest you most (e.g., FinTech, Health, EdTech)?")
	return questions


def propose_skill_validation_tasks(user: UserProfile) -> List[ValidationTask]:
	tasks: List[ValidationTask] = []
	top_skills = [s.skill_name for s in (user.skills or [])][:3]
	for skill in top_skills:
		tasks.append(
			ValidationTask(
				title=f"Build a micro-project in {skill}",
				description=f"Create a weekend-sized project showcasing {skill}. Include README and a short demo.",
				related_skill=skill,
				expected_outcome="Public repo with README, small demo (GIF/video), and a short write-up.",
				difficulty="Medium",
			)
		)
	if not tasks:
		tasks.append(
			ValidationTask(
				title="Create a portfolio README",
				description="Draft a GitHub profile README summarizing your skills, projects, and goals.",
				expected_outcome="A clear README with links to 2–3 projects and contact info.",
			)
		)
	return tasks


def _default_confirm(_: str) -> str:
	# Default to Deferred if no callback is provided
	return ApprovalDecision.DEFERRED


def _default_ask(_: str) -> str:
	return ""


def run_interaction(
	user: UserProfile,
	github_extract: Any = None,
	linkedin_extract: Any = None,
	hf_models: Optional[List[Any]] = None,
	ask: Callable[[str], str] = _default_ask,
	confirm: Callable[[str], str] = _default_confirm,
	save_profile: Optional[Callable[[UserProfile], None]] = None,
	log_event: Optional[Callable[[InteractionEvent], None]] = None,
	tune_trend_model: Optional[Callable[[Dict[str, Any]], None]] = None,
) -> Dict[str, Any]:
	"""Orchestrate a user interaction cycle:
	1) Ask personalized questions to enrich the profile
	2) Present recommendations and collect approval/feedback
	3) Propose validation tasks for existing skills with approval
	Applies updates and optionally persists/logs via callbacks.
	Returns a dict with updated profile, questions asked, decisions, and tasks.
	"""

	logs: List[InteractionEvent] = []

	# 1) Personalized questions
	questions = generate_personalized_questions(user)
	answers: Dict[str, str] = {}
	for q in questions:
		ans = ask(q) if ask else ""
		answers[q] = ans
		evt = InteractionEvent(event_type="question", message=q, payload={"answer": ans})
		logs.append(evt)
		if log_event:
			log_event(evt)

	# Apply simple enrichments from answers (lightweight parsing)
	if answers.get("What's your current city and country?") and not user.location:
		user.location = answers["What's your current city and country?"]

	# 2) Build/align and get recommendations
	aligned, recs = process_extractions_and_recommend(
		user,
		github=github_extract,
		linkedin=linkedin_extract,
		hf_models=hf_models,
	)

	# Present recs and gather approvals
	decisions: List[Tuple[CareerActionRecommendation, str]] = []
	for rec in recs:
		prompt = (
			f"Recommendation: {rec.title}\n"
			f"Why: {rec.reason or ''}\n"
			f"Actions: {', '.join(rec.suggested_actions)}\n"
			"Approve, Defer, or Reject?"
		)
		decision = confirm(prompt) if confirm else ApprovalDecision.DEFERRED
		rec.approval_status = decision
		decisions.append((rec, decision))
		evt = InteractionEvent(event_type="recommendation_decision", message=rec.title, payload={"decision": decision})
		logs.append(evt)
		if log_event:
			log_event(evt)

	# 3) Propose validation tasks and seek approval
	tasks = propose_skill_validation_tasks(aligned)
	approved_tasks: List[ValidationTask] = []
	for task in tasks:
		decision = confirm(f"Task: {task.title}\n{task.description}\nApprove?") if confirm else ApprovalDecision.DEFERRED
		evt = InteractionEvent(event_type="task_decision", message=task.title, payload={"decision": decision})
		logs.append(evt)
		if log_event:
			log_event(evt)
		if decision == ApprovalDecision.APPROVED:
			approved_tasks.append(task)
			# Optionally add a planned project entry
			aligned.projects.append(
				Projects(
					name=f"Planned: {task.title}",
					description=task.description,
					technologies=[task.related_skill] if task.related_skill else [],
					link=None,
					interactions=None,
				)
			)

	# Persist updates
	if save_profile:
		save_profile(aligned)

	# Optional: provide feedback to trend model (e.g., approvals/deferals)
	if tune_trend_model:
		tune_trend_model(
			{
				"approved_recs": [r.title for r, d in decisions if d == ApprovalDecision.APPROVED],
				"deferred_recs": [r.title for r, d in decisions if d == ApprovalDecision.DEFERRED],
				"rejected_recs": [r.title for r, d in decisions if d == ApprovalDecision.REJECTED],
			}
		)

	return {
		"updated_profile": aligned,
		"questions": questions,
		"answers": answers,
		"recommendations": recs,
		"decisions": [(r.title, d) for r, d in decisions],
		"approved_tasks": approved_tasks,
		"logs": logs,
	}

