from pydantic import BaseModel, Field
from typing import List, Optional

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












