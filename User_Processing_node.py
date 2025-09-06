from pydantic import BaseModel, Field
from schemas import UserProfile
from typing import List, Optional

from typing import List, Optional, Union
from pydantic import BaseModel, Field

# --- Sub-models remain largely the same, with corrected naming ---

class LinkedInPost(BaseModel):
    content: str
    likes: int = Field(default=0, ge=0)
    comments: int = Field(default=0, ge=0)
    shares: int = Field(default=0, ge=0)
    tags: List[str] = Field(default_factory=list)

class College(BaseModel):
    name: str
    degree: str
    field_of_study: str
    cgpa: Optional[float] = Field(default=None, ge=0.0, le=10.0, alias="CGPA") # Use alias if input is capitalized
    start_year: int
    end_year: int
    education_type: str = "College" # Add a literal type for easy identification

class School(BaseModel):
    name: str
    class_name: str
    subjects_taken: Optional[str] = None
    marks_percentage: Optional[float] = Field(default=None, ge=0.0, le=100.0, alias="Marks") # Renamed for clarity
    start_year: int
    end_year: int
    education_type: str = "School" # Add a literal type



class LinkedInProfileOutput(BaseModel):
    username: str
    email: str
    headline: str
    location: str
    connections: int = Field(default=0, ge=0)
    skills: List[str] = Field(default_factory=list)

    
    education: List[Union[College, School]] = Field(default_factory=list)

    post_impressions: int = Field(default=0, ge=0) # <-- RENAMED from postimpression
    post_count: int = Field(default=0, ge=0) # <-- RENAMED from no_of_posts
    followers_count: int = Field(default=0, ge=0) # <-- RENAMED from Followers_count
    profile_viewers: int = Field(default=0, ge=0)
    meaningful_connections: int = Field(default=0, ge=0)
    search_appearances: int = Field(default=0, ge=0)
    profile_strength: int = Field(default=0, ge=0, le=100)
    
    posts: Optional[List[LinkedInPost]] = Field(default_factory=list)
    certifications: Optional[List[str]] = Field(default_factory=list) # <-- RENAMED
    honors_and_awards: Optional[List[str]] = Field(default_factory=list) # <-- RENAMED 



class GitHubRepositoryOutput(BaseModel):
    repository_name: str = Field(description="The name of the GitHub repository")
    description: str = Field(description="The description of the GitHub repository")
    forks: int = Field(default=0, ge=0)
    stars: int = Field(default=0, ge=0)
    url: str = Field(description="The URL of the GitHub repository")
    last_updated: str = Field(description="The last updated date of the GitHub repository")

class GitHubUserOutput(BaseModel):
    username: str = Field(description="The username of the GitHub user")
    bio: Optional[str] = Field(default=None, description="The bio of the GitHub user")
    email: str = Field(description="The email of the GitHub user")
    company: Optional[List[str]] = Field(default_factory=list, description="List of companies the user has worked at")
    location: Optional[str] = Field(default=None, description="The location of the GitHub user")
    blog: Optional[str] = Field(default=None, description="The blog or website of the GitHub user")
    repositories: List[GitHubRepositoryOutput] = Field(default_factory=list, description="List of repositories owned by the user")
    no_of_repositories: int = Field(default=0, ge=0, description="Total number of repositories")
    forks_count: int = Field(default=0, ge=0, description="Total number of forks across all repositories")
    stars_count: int = Field(default=0, ge=0, description="Total number of stars across all repositories")
    viewers_count: int = Field(default=0, ge=0, description="Total number of viewers across all repositories")
    contributions_count: int = Field(default=0, ge=0, description="Total number of contributions across all repositories")
    followers_count: int = Field(default=0, ge=0, description="Total number of followers of the GitHub user")
    following_count: int = Field(default=0, ge=0, description="Total number of users followed by the GitHub user")
    twitter: Optional[str] = Field(default=None, description="The Twitter handle of the GitHub user")
    



class LinkedInPost(BaseModel):
    content: str
    likes: int = Field(default=0, ge=0, description="Number of likes on the post")
    comments: int = Field(default=0, ge=0, description="Number of comments on the post")
    shares: int = Field(default=0, ge=0, description="Number of shares of the post")
    tags: List[str] = Field(default_factory=list, description="List of tags associated with the post")



def build_linkedin_profile_output_from_analysis(analysis: dict) -> LinkedInProfileOutput:
    """Build a LinkedInProfileOutput object from an analysis dict.

    Accepts both normalized keys (post_impressions, post_count, certifications, honors_and_awards)
    and alternate keys that might come from other tools (postimpression, no_of_posts, Certifications, Honorsawards),
    and can handle education provided as either:
      - a list of dicts with "Colleges" and/or "Schools" arrays, or
      - a flat list of College/School-like dicts.
    """
    data = analysis or {}

    username = data.get("username", "")
    email = data.get("email", "")
    headline = data.get("headline", "")
    location = data.get("location", "")
    connections = int(data.get("connections") or 0)

    # Counts with fallbacks for alternate key names
    post_impressions = int(data.get("post_impressions") or data.get("postimpression") or 0)
    post_count = int(data.get("post_count") or data.get("no_of_posts") or 0)
    followers_count = int(data.get("followers_count") or data.get("Followers_count") or 0)
    profile_viewers = int(data.get("profile_viewers") or 0)
    meaningful_connections = int(data.get("meaningful_connections") or 0)
    search_appearances = int(data.get("search_appearances") or 0)
    profile_strength = int(data.get("profile_strength") or 0)

    # Skills
    raw_skills = data.get("skills") or []
    skills: List[str] = [str(s) for s in raw_skills if isinstance(s, (str, int, float))]

    # Education handling
    edu_items: List[Union[College, School]] = []
    raw_education = data.get("education") or []
    if isinstance(raw_education, list):
        for entry in raw_education:
            if not isinstance(entry, dict):
                continue
            # Nested shape: { "Colleges": [...], "Schools": [...] }
            colleges = entry.get("Colleges") or entry.get("colleges") or []
            schools = entry.get("Schools") or entry.get("schools") or []
            if colleges or schools:
                for c in colleges:
                    if isinstance(c, dict):
                        try:
                            edu_items.append(College(**c))
                        except Exception:
                            # Minimal safe mapping
                            edu_items.append(College(
                                name=c.get("name", ""),
                                degree=c.get("degree", ""),
                                field_of_study=c.get("field_of_study", ""),
                                cgpa=c.get("CGPA"),
                                start_year=int(c.get("start_year") or 0),
                                end_year=int(c.get("end_year") or 0),
                            ))
                for s in schools:
                    if isinstance(s, dict):
                        try:
                            edu_items.append(School(**s))
                        except Exception:
                            edu_items.append(School(
                                name=s.get("name", ""),
                                class_name=s.get("class_name", ""),
                                subjects_taken=s.get("subjects_taken"),
                                marks_percentage=s.get("Marks"),
                                start_year=int(s.get("start_year") or 0),
                                end_year=int(s.get("end_year") or 0),
                            ))
            else:
                # Flat shape: try to detect by keys
                if "degree" in entry or "field_of_study" in entry:
                    try:
                        edu_items.append(College(**entry))
                    except Exception:
                        edu_items.append(College(
                            name=entry.get("name", ""),
                            degree=entry.get("degree", ""),
                            field_of_study=entry.get("field_of_study", ""),
                            cgpa=entry.get("CGPA"),
                            start_year=int(entry.get("start_year") or 0),
                            end_year=int(entry.get("end_year") or 0),
                        ))
                elif "class_name" in entry or "Marks" in entry or "marks_percentage" in entry:
                    try:
                        edu_items.append(School(**entry))
                    except Exception:
                        edu_items.append(School(
                            name=entry.get("name", ""),
                            class_name=entry.get("class_name", ""),
                            subjects_taken=entry.get("subjects_taken"),
                            marks_percentage=entry.get("Marks") or entry.get("marks_percentage"),
                            start_year=int(entry.get("start_year") or 0),
                            end_year=int(entry.get("end_year") or 0),
                        ))

    # Posts
    posts_list: List[LinkedInPost] = []
    for p in data.get("posts", []) or []:
        if isinstance(p, dict):
            try:
                posts_list.append(LinkedInPost(**p))
            except Exception:
                posts_list.append(LinkedInPost(
                    content=str(p.get("content", "")),
                    likes=int(p.get("likes") or 0),
                    comments=int(p.get("comments") or 0),
                    shares=int(p.get("shares") or 0),
                    tags=p.get("tags") or [],
                ))

    # Certifications and honors
    certifications = data.get("certifications") or data.get("Certifications") or []
    honors_and_awards = data.get("honors_and_awards") or data.get("Honorsawards") or []

    return LinkedInProfileOutput(
        username=username,
        email=email,
        headline=headline,
        location=location,
        connections=connections,
        skills=skills,
        education=edu_items,
        post_impressions=post_impressions,
        post_count=post_count,
        followers_count=followers_count,
        profile_viewers=profile_viewers,
        meaningful_connections=meaningful_connections,
        search_appearances=search_appearances,
        profile_strength=profile_strength,
        posts=posts_list,
        certifications=certifications,
        honors_and_awards=honors_and_awards,
    )


from hard_coding_instead_scrap import github_user_output, linked_in_user_output

def User_report(github_user_output: GitHubUserOutput, linked_in_user_output: LinkedInProfileOutput) -> UserProfile:
    # Basic info
    user_profile = UserProfile(
        id=1,  # Placeholder, should be set appropriately
        email=github_user_output.email or linked_in_user_output.email or "<Email Not Found>",
        name=github_user_output.username or linked_in_user_output.username or "<Name Not Found>",
        bio=github_user_output.bio or linked_in_user_output.headline or "<Bio Not Found>",
        location=github_user_output.location or linked_in_user_output.location or "<Location Not Found>",
        skills=github_user_output.skills or linked_in_user_output.skills or [],
        education=github_user_output.education or linked_in_user_output.education or [],
        work_experience=github_user_output.work_experience or linked_in_user_output.work_experience or [],
        achievements=github_user_output.achievements or linked_in_user_output.honors_and_awards or [],
        certifications=github_user_output.certifications or linked_in_user_output.certifications or [],
    )
    return user_profile


from sqlalchemy import create_engine, Column, Integer, String, JSON
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class UserDB(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)
    profile_data = Column(JSON) # Store the full UserProfile dict here

import chromadb
from sentence_transformers import SentenceTransformer

# 1. Initialize models and DB
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
vector_db_client = chromadb.Client()
profiles_collection = vector_db_client.create_collection(name="user_profiles")

# 2. Assume you have a user_profile object from your 'User_report' function
# Let's say it's for user with id=1
user_profile = User_report(github_user_output, linked_in_user_output)

# 3. Use an LLM to generate a rich summary (conceptual)
def get_llm_summary(profile: UserProfile) -> str:
    # In a real app, you'd call an API like OpenAI or Gemini here
    prompt = f"""
    Analyze the following professional profile and generate a concise, third-person professional summary.
    Highlight their key strengths, primary domain (e.g., "Full-Stack Development," "Data Science"), 
    and core technologies.

    Name: {profile.name}
    Bio: {profile.bio}
    Skills: {', '.join(profile.skills)}
    Projects: {profile.projects} 
    ---
    Professional Summary:
    """
    # This is a mock response
    summary = (f"{profile.name} is a skilled software developer specializing in backend systems. "
               f"They have extensive experience with Python and cloud services, demonstrated through "
               f"numerous projects. Key strengths include API design, database management, and DevOps practices.")
    return summary

llm_summary = get_llm_summary(user_profile)
print("LLM-Generated Summary:", llm_summary)

# 4. Create the vector embedding from the summary
embedding = embedding_model.encode(llm_summary).tolist()

# 5. Store the embedding and metadata in the vector DB
profiles_collection.add(
    embeddings=[embedding],
    documents=[llm_summary], # Store the text for context
    metadatas=[{"name": user_profile.name, "email": user_profile.email}],
    ids=[str(user_profile.id)] # Use the ID from your standard DB
)

print("\nProfile stored in vector database!")