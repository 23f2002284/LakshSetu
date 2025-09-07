from pydantic import BaseModel, Field
from schemas import UserProfile, Certifications, Skills
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



def User_report(github_user_output: GitHubUserOutput, linked_in_user_output: LinkedInProfileOutput) -> UserProfile:
    # Normalize skills (str -> Skills model)
    normalized_skills: List[Skills] = []
    for s in linked_in_user_output.skills or []:
        try:
            normalized_skills.append(Skills(skill_name=str(s), skill_strength="Unknown"))
        except Exception:
            # Skip any malformed entries
            continue

    # Normalize certifications (str -> Certifications model)
    normalized_certs: List[Certifications] = []
    for c in linked_in_user_output.certifications or []:
        if isinstance(c, str):
            normalized_certs.append(
                Certifications(title=c, issuer="LinkedIn", issued_date="")
            )
        elif isinstance(c, dict):
            try:
                normalized_certs.append(Certifications(**c))
            except Exception:
                # Fallback minimal mapping
                normalized_certs.append(
                    Certifications(title=str(c.get("title") or ""), issuer=str(c.get("issuer") or ""), issued_date=str(c.get("issued_date") or ""))
                )

    user_profile = UserProfile(
        id=1,  # Placeholder, should be set appropriately
        email=github_user_output.email or linked_in_user_output.email or "<Email Not Found>",
        name=github_user_output.username or linked_in_user_output.username or "<Name Not Found>",
        bio=github_user_output.bio or linked_in_user_output.headline or "<Bio Not Found>",
        location=github_user_output.location or linked_in_user_output.location or "<Location Not Found>",
        skills=normalized_skills or None,
        # education field not present in UserProfile schema; omit to avoid extra
        work_experience=getattr(linked_in_user_output, "work_experience", []) or None,
        achievements=linked_in_user_output.honors_and_awards or None,
        certifications=normalized_certs or None,
    )
    return user_profile



# from sqlalchemy import create_engine, Column, Integer, String, JSON
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.ext.declarative import declarative_base



# # 1. First create the engine
# SQLALCHEMY_DATABASE_URL = "sqlite:///./users.db"
# engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# # 2. Then create SessionLocal (this needs engine to exist)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# # SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base = declarative_base()

# class UserDB(Base):
#     __tablename__ = 'users'
#     id = Column(Integer, primary_key=True)
#     name = Column(String)
#     email = Column(String, unique=True)
#     profile_data = Column(JSON) # Store the full UserProfile dict here


# # engine = create_engine('sqlite:///users.db') 
# Base.metadata.create_all(bind=engine)


# import chromadb
# from sentence_transformers import SentenceTransformer

# 1. Initialize models and DB
# embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

# # Use a persistent Chroma client and reuse the same collection across runs
# _PERSIST_DIR = "./.chromadb"
# vector_db_client = chromadb.PersistentClient(path=_PERSIST_DIR)
# profiles_collection = vector_db_client.get_or_create_collection(name="user_profiles")


# Note: Demo code that builds a profile from hard-coded examples was removed
# to avoid circular imports. Use the notebook or a separate runner script
# to import from `hard_coded_examples` and call `User_report`.