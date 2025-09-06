from schemas import (
    GitHubRepoExtract,
    GitHubUserExtract,
    LinkedInEducationExtract,
    LinkedInPostExtract,
    LinkedInProfileExtract,
    HuggingFaceModelExtract,
    XPostExtract,
    ArxivPaperExtract,
    TrendSkillExtract,
    MediumArticleExtract,
    StackOverflowProfileExtract,
    GoogleScholarPublicationExtract,
    CareerActionRecommendation
)
from pydantic import BaseModel
from typing import List, Optional
from schemas import UserProfile, Skills, Projects, Certifications
# --- Alignment + Recommendation pipeline ---

def _safe_model_dump(model: BaseModel) -> dict:
    return model.model_dump() if hasattr(model, "model_dump") else model.dict()


def _project_from_github_repo(repo: GitHubRepoExtract) -> Projects:
    techs = [repo.primary_language] if repo.primary_language else []
    interactions = []
    if repo.metrics.stars:
        interactions.append(f"Stars: {repo.metrics.stars}")
    if repo.metrics.forks:
        interactions.append(f"Forks: {repo.metrics.forks}")
    if repo.metrics.impressions:
        interactions.append(f"Impressions: {repo.metrics.impressions}")
    interactions_str = ", ".join(interactions) if interactions else None
    return Projects(
        name=repo.name,
        description=repo.description or "",
        technologies=techs,
        link=str(repo.url),
        interactions=interactions_str,
        skills_used=None,
    )


def _merge_projects(existing: List[Projects], new: List[Projects]) -> List[Projects]:
    by_name = {p.name.lower(): p for p in existing}
    for p in new:
        key = p.name.lower()
        if key in by_name:
            # Merge technologies and keep first description/link
            merged = by_name[key]
            merged.techniques = list(set(merged.technologies + p.technologies)) if hasattr(merged, 'technologies') else merged.technologies
            if not merged.link and p.link:
                merged.link = p.link
            if not merged.interactions and p.interactions:
                merged.interactions = p.interactions
        else:
            by_name[key] = p
    return list(by_name.values())


def _merge_skills(existing: List[Skills], new_names: List[str], default_strength: str = "Medium") -> List[Skills]:
    if not existing:
        existing = []
    have = {s.skill_name.lower(): s for s in existing}
    for n in new_names:
        key = str(n).strip()
        if not key:
            continue
        lk = key.lower()
        if lk not in have:
            have[lk] = Skills(skill_name=key, skill_strength=default_strength)
    return list(have.values())


def align_extractions_with_profile(
    user: UserProfile,
    github: Optional[GitHubUserExtract] = None,
    linkedin: Optional[LinkedInProfileExtract] = None,
    hf_models: Optional[List[HuggingFaceModelExtract]] = None,
) -> UserProfile:
    """Return an updated UserProfile by aligning extracted data from sources."""
    data = _safe_model_dump(user)
    updated = UserProfile(**data)

    # Map GitHub
    if github:
        updated.github = github.username or updated.github
        # Projects from repos
        gh_projects = [_project_from_github_repo(r) for r in (github.repositories or [])]
        updated.projects = _merge_projects(updated.projects or [], gh_projects)
        # Skills from repo primary languages (heuristic)
        gh_skills = [r.primary_language for r in (github.repositories or []) if r.primary_language]
        updated.skills = _merge_skills(updated.skills or [], gh_skills)
        # Website/blog
        if github.blog and not updated.website:
            updated.website = str(github.blog)

    # Map LinkedIn
    if linkedin:
        updated.linkedin = linkedin.username or updated.linkedin
        if linkedin.location and not updated.location:
            updated.location = linkedin.location
        # Skills
        updated.skills = _merge_skills(updated.skills or [], linkedin.skills or [])
        # Certifications -> convert to Certifications models (issuer unknown)
        new_certs = [
            Certifications(title=title, issuer="LinkedIn", issued_date="Unknown")
            for title in (linkedin.certifications or [])
        ]
        updated.certifications = (updated.certifications or []) + new_certs if new_certs else updated.certifications

    # Map Hugging Face (treat model task/tags as skills)
    if hf_models:
        hf_skill_names: List[str] = []
        for m in hf_models:
            if m.task:
                hf_skill_names.append(m.task)
            hf_skill_names.extend(m.tags or [])
        updated.skills = _merge_skills(updated.skills or [], hf_skill_names)

    return updated


def suggest_next_steps(
    user: UserProfile,
    github: Optional[GitHubUserExtract] = None,
    linkedin: Optional[LinkedInProfileExtract] = None,
) -> List[CareerActionRecommendation]:
    """Suggest prioritized next actions based on profile and recent extractions."""
    recs: List[CareerActionRecommendation] = []

    # 1) Skill gap suggestions (vs. simple heuristic trending list)
    trending = ["AI/ML", "Generative AI", "Cloud-Native", "MLOps", "Data Engineering", "Cybersecurity"]
    if user.skills:
        user_skill_names = {s.skill_name.lower() for s in user.skills}
        gaps = [t for t in trending if t.lower() not in user_skill_names]
        if gaps:
            recs.append(CareerActionRecommendation(
                title="Close top skill gaps",
                description=f"Focus on: {', '.join(gaps[:3])}",
                reason="In-demand skills not present in profile",
                priority=1,
                suggested_actions=[
                    f"Take a short course on {gaps[0]}" if gaps else "",
                    "Build a weekend project demonstrating the skill",
                    "Share a LinkedIn post about what you learned",
                ],
            ))

    # 2) GitHub recency-driven suggestions
    if github and github.repositories:
        # Find most recently updated repo
        most_recent = None
        for r in github.repositories:
            if r.last_updated and (most_recent is None or (r.last_updated > most_recent.last_updated)):
                most_recent = r
        if most_recent:
            recs.append(CareerActionRecommendation(
                title="Polish your most recent repo",
                description=f"Improve README and add a demo to {most_recent.name}",
                reason="Recent work is easiest to showcase for quick wins",
                priority=2,
                suggested_actions=[
                    "Add a clear README with setup, features, and screenshots",
                    "Publish a short demo video (GIF or Loom) and link it",
                    "Pin the repo and share on LinkedIn",
                ],
            ))

    # 3) LinkedIn activity suggestions
    if linkedin:
        if (linkedin.post_count or 0) == 0:
            recs.append(CareerActionRecommendation(
                title="Post on LinkedIn",
                description="Write a short post summarizing a recent learning or project",
                reason="Zero posts — build visibility",
                priority=2,
                suggested_actions=[
                    "Share a 150–200 word post with a screenshot",
                    "Add relevant hashtags",
                    "Cross-link to your GitHub project",
                ],
            ))
        if (linkedin.connections or 0) < 200:
            recs.append(CareerActionRecommendation(
                title="Grow your network",
                description="Connect with alumni and peers in your field",
                reason="Under 200 connections typically limits reach",
                priority=3,
                suggested_actions=[
                    "Send 5 personalized connection requests to alumni",
                    "Join 1–2 relevant LinkedIn groups",
                ],
            ))

    # 4) Certification utilization
    if user.certifications and not user.projects:
        recs.append(CareerActionRecommendation(
            title="Turn a certification into a project",
            description="Build a small project applying your certified skill",
            reason="Projects demonstrate practical ability",
            priority=2,
            suggested_actions=[
                "Scope a 1–2 week build",
                "Write a blog/README on the approach and results",
            ],
        ))

    return recs


def process_extractions_and_recommend(
    user: UserProfile,
    github: Optional[GitHubUserExtract] = None,
    linkedin: Optional[LinkedInProfileExtract] = None,
    hf_models: Optional[List[HuggingFaceModelExtract]] = None,
) -> tuple[UserProfile, List[CareerActionRecommendation]]:
    """End-to-end: align extractions into the profile and produce next-step recommendations."""
    aligned = align_extractions_with_profile(user, github=github, linkedin=linkedin, hf_models=hf_models)
    recs = suggest_next_steps(aligned, github=github, linkedin=linkedin)
    aligned.recommendations = [r.title for r in recs]
    return aligned, recs













