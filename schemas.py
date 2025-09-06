from pydantic import BaseModel, Field, HttpUrl
from typing import List, Optional
from enum import Enum
from datetime import datetime

class Certifications(BaseModel):
    title: str
    issuer: str
    issued_date: str
    credential_id: Optional[str] = Field(default=None)
    tags: List[str] = Field(default_factory=list)
    certificate_strength: Optional[str] = Field(default=None, description="The strength of the certificate e.g., 'High', 'Medium', 'Low'")

class Projects(BaseModel):
    name: str
    description: str
    technologies: List[str] = Field(default_factory=list)
    link: Optional[str] = Field(default=None)
    interactions: Optional[str] = Field(default=None, description="e.g., 'Starred on GitHub', 'Forked on GitHub', 'Contributed via PR', views, clicks, likes")
    skills_used: Optional[List[str]] = Field(default=None)

class Blogs(BaseModel):
    title: str
    content: str
    published_date: str
    tags: List[str] = Field(default_factory=list)
    interactions: Optional[str] = Field(default=None, description="e.g., views, clicks, likes")
    strength: Optional[str] = Field(default=None, description="The strength of the content e.g., 'High', 'Medium', 'Low'")

class Mentions(BaseModel):
    mention_name: str
    mention_context: str
    mention_strength: Optional[str] = Field(default=None, description="The strength of the mention e.g., 'High', 'Medium', 'Low'")

class Network(BaseModel):
    connection_name: str
    connection_strength: int = Field(default=0, ge=0)
    connection_context: str
    relation: Optional[str] = Field(default=None, description="e.g., 'Colleague', 'Mentor', 'Peer'")

class Skills(BaseModel):
    skill_name: str
    skill_strength: str
    implemented_projects: List[Projects] = Field(default_factory=list)
    implemented_blogs: Optional[List[Blogs]] = Field(default=None)
    achievements_of_skills: Optional[List[str]] = Field(default=None)
    mentions: Optional[List[Mentions]] = Field(default=None, description="Names of influential people or organizations that mentioned the user in relation to this skill")
    influencial_network: Optional[List[str]] = Field(default=None)
    network_strength: int = Field(default=0, ge=0)

class UserProfile(BaseModel):
    id: int
    email: str
    name: str
    age: Optional[int] = Field(default=None, ge=0)
    location: Optional[str] = Field(default=None)
    github: Optional[str] = Field(default=None)
    linkedin: Optional[str] = Field(default=None)
    huggingface: Optional[str] = Field(default=None)
    x: Optional[str] = Field(default=None)
    website: Optional[str] = Field(default=None)
    certifications: Optional[List[Certifications]] = Field(default=None)
    skills: Optional[List[Skills]] = Field(default=None)
    projects: List[Projects] = Field(default_factory=list)
    blogs: Optional[List[Blogs]] = Field(default=None)
    achievements: Optional[List[str]] = Field(default=None)
    trending_skills: Optional[List[str]] = Field(default=None, description="Skills currently trending in the tech industry")
    skill_gap_analysis: Optional[dict] = Field(default=None, description="Analysis of gaps between user's skills and trending skills")
    recommendations: Optional[List[str]] = Field(default=None, description="Personalized career suggestions")
    network_opportunities: Optional[List[str]] = Field(default=None, description="Suggested people or communities to connect with")

def analyze_skill_gaps(user_skills, trending_skills):
    user_skill_names = {skill.skill_name for skill in user_skills}
    missing_skills = set(trending_skills) - user_skill_names
    return list(missing_skills)



## --- Schemas for Trend fetching and matching with User Profiles and User Goal

# --- Shared primitives for high-quality, source-specific extraction ---

class DataSource(str, Enum):
    github = "github"
    linkedin = "linkedin"
    huggingface = "huggingface"
    kaggle = "kaggle"
    google_scholar = "google_scholar"
    stack_overflow = "stack_overflow"
    arxiv = "arxiv"
    medium = "medium"
    x = "x"  
    website = "website"


class ExtractionMeta(BaseModel):
    source: DataSource
    source_url: Optional[HttpUrl] = None
    fetched_at: datetime = Field(default_factory=datetime.utcnow, description="UTC timestamp when data was fetched")


class EngagementMetrics(BaseModel):
    views: int = Field(default=0, ge=0)
    likes: int = Field(default=0, ge=0)
    comments: int = Field(default=0, ge=0)
    shares: int = Field(default=0, ge=0)
    stars: int = Field(default=0, ge=0)
    forks: int = Field(default=0, ge=0)
    impressions: int = Field(default=0, ge=0)


# --- GitHub extraction schemas ---

class GitHubRepoExtract(BaseModel):
    name: str
    description: Optional[str] = ""
    url: HttpUrl
    primary_language: Optional[str] = None
    last_updated: Optional[datetime] = None
    metrics: EngagementMetrics = Field(default_factory=EngagementMetrics)


class GitHubUserExtract(BaseModel):
    username: str
    name: Optional[str] = None
    bio: Optional[str] = None
    companies: List[str] = Field(default_factory=list)
    location: Optional[str] = None
    blog: Optional[HttpUrl] = None
    twitter: Optional[str] = None
    public_repos: int = Field(default=0, ge=0)
    followers: int = Field(default=0, ge=0)
    following: int = Field(default=0, ge=0)
    repositories: List[GitHubRepoExtract] = Field(default_factory=list)
    meta: ExtractionMeta


# --- LinkedIn extraction schemas ---

class LinkedInEducationExtract(BaseModel):
    school: str
    degree: Optional[str] = None
    field_of_study: Optional[str] = None
    start_year: Optional[int] = Field(default=None, ge=1900)
    end_year: Optional[int] = Field(default=None, ge=1900)
    grade: Optional[str] = None


class LinkedInPostExtract(BaseModel):
    content: str
    posted_at: Optional[datetime] = None
    tags: List[str] = Field(default_factory=list)
    metrics: EngagementMetrics = Field(default_factory=EngagementMetrics)


class LinkedInProfileExtract(BaseModel):
    username: str
    email: Optional[str] = None
    headline: Optional[str] = None
    location: Optional[str] = None
    connections: int = Field(default=0, ge=0)
    skills: List[str] = Field(default_factory=list)
    education: List[LinkedInEducationExtract] = Field(default_factory=list)
    posts: List[LinkedInPostExtract] = Field(default_factory=list)
    followers_count: int = Field(default=0, ge=0)
    profile_viewers: int = Field(default=0, ge=0)
    meaningful_connections: int = Field(default=0, ge=0)
    search_appearances: int = Field(default=0, ge=0)
    post_impressions: int = Field(default=0, ge=0)
    post_count: int = Field(default=0, ge=0)
    profile_strength: int = Field(default=0, ge=0, le=100)
    certifications: List[str] = Field(default_factory=list)
    honors_and_awards: List[str] = Field(default_factory=list)
    meta: ExtractionMeta


# --- Hugging Face extraction schemas ---

class HuggingFaceModelExtract(BaseModel):
    model_id: str
    task: Optional[str] = None
    url: Optional[HttpUrl] = None
    likes: int = Field(default=0, ge=0)
    downloads: int = Field(default=0, ge=0)
    last_modified: Optional[datetime] = None
    tags: List[str] = Field(default_factory=list)
    meta: ExtractionMeta


# --- Stack Overflow extraction schemas ---

class StackOverflowProfileExtract(BaseModel):
    display_name: str
    reputation: int = Field(default=0, ge=0)
    badges: dict = Field(default_factory=dict, description="e.g., {'gold': 1, 'silver': 2, 'bronze': 3}")
    answers: int = Field(default=0, ge=0)
    questions: int = Field(default=0, ge=0)
    top_tags: List[str] = Field(default_factory=list)
    profile_url: Optional[HttpUrl] = None
    meta: ExtractionMeta


# --- Google Scholar extraction schemas ---

class GoogleScholarPublicationExtract(BaseModel):
    title: str
    url: Optional[HttpUrl] = None
    authors: List[str] = Field(default_factory=list)
    venue: Optional[str] = None
    year: Optional[int] = Field(default=None, ge=1900)
    citations: int = Field(default=0, ge=0)
    meta: ExtractionMeta


# --- arXiv extraction schemas ---

class ArxivPaperExtract(BaseModel):
    title: str
    url: Optional[HttpUrl] = None
    authors: List[str] = Field(default_factory=list)
    published_at: Optional[datetime] = None
    categories: List[str] = Field(default_factory=list)
    summary: Optional[str] = None
    citations: Optional[int] = Field(default=None, ge=0)
    meta: ExtractionMeta


# --- Medium/Blog extraction schemas ---

class MediumArticleExtract(BaseModel):
    title: str
    url: HttpUrl
    published_at: Optional[datetime] = None
    tags: List[str] = Field(default_factory=list)
    metrics: EngagementMetrics = Field(default_factory=EngagementMetrics)
    meta: ExtractionMeta


# --- X (Twitter) extraction schemas ---

class XPostExtract(BaseModel):
    content: str
    url: Optional[HttpUrl] = None
    created_at: Optional[datetime] = None
    metrics: EngagementMetrics = Field(default_factory=EngagementMetrics)
    meta: ExtractionMeta


# --- Trends/Recommendations helpers ---

class TrendSkillExtract(BaseModel):
    name: str
    score: float = Field(default=0.0, ge=0.0)
    sources: List[DataSource] = Field(default_factory=list)
    meta: Optional[ExtractionMeta] = None


class CareerRecommendation(BaseModel):
    title: str
    reason: Optional[str] = None
    priority: int = Field(default=3, ge=1, le=5, description="1=highest priority, 5=lowest")
    suggested_actions: List[str] = Field(default_factory=list)


class TrendProfile(BaseModel):






