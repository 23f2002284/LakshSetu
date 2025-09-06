from pydantic import BaseModel, Field
from LakshSetu.schemas import UserProfile
from typing import List, Optional


class GitHubRepositoryOutput(BaseModel):
    repository_name: str = Field(description="The name of the GitHub repository")
    description: str = Field(description="The description of the GitHub repository")
    forks: int = Field(default=0, ge=0)
    stars: int = Field(default=0, ge=0)

class GitHubUserOutput(BaseModel):
    username: str = Field(description="The username of the GitHub user")
    email: str = Field(description="The email of the GitHub user")
    repositories: List[GitHubRepositoryOutput] = Field(default_factory=list, description="List of repositories owned by the user")
    no_of_repositories: int = Field(default=0, ge=0, description="Total number of repositories")
    forks_count: int = Field(default=0, ge=0, description="Total number of forks across all repositories")
    stars_count: int = Field(default=0, ge=0, description="Total number of stars across all repositories")
    viewers_count: int = Field(default=0, ge=0, description="Total number of viewers across all repositories")
    contributions_count: int = Field(default=0, ge=0, description="Total number of contributions across all repositories")
    followers_count: int = Field(default=0, ge=0, description="Total number of followers of the GitHub user")
    following_count: int = Field(default=0, ge=0, description="Total number of users followed by the GitHub user")



class LinkedInPost(BaseModel):
    content: str
    likes: int = Field(default=0, ge=0, description="Number of likes on the post")
    comments: int = Field(default=0, ge=0, description="Number of comments on the post")
    shares: int = Field(default=0, ge=0, description="Number of shares of the post")
    tags: List[str] = Field(default_factory=list, description="List of tags associated with the post")


class LinkedInProfileOutput(BaseModel):
    username: str
    headline: str
    location: str
    connections: int = Field(default=0, ge=0, description="Number of connections")
    skills: List[str] = Field(default_factory=list, description="List of skills")
    education: List[str] = Field(default_factory=list, description="List of educational qualifications")
    postimpression: int = Field(default=0, ge=0, description="Total number of impressions on all posts")
    no_of_posts: int = Field(default=0, ge=0, description="Total number of posts")
    Followers_count: int = Field(default=0, ge=0, description="Total number of followers")
    profile_viewers: int = Field(default=0, ge=0, description="Total number of profile viewers")
    meaningful_connections: int = Field(default=0, ge=0, le=Followers_count,description="Number of meaningful connections having influencial network")
    search_appearances: int = Field(default=0, ge=0, description="Total number of times the profile appeared in searches")
    posts: Optional[List[LinkedInPost]] = Field(default_factory=list, description="List of posts made by the user")
    profile_strength: int = Field(default=0, ge=0, le=100, description="Profile strength as a percentage")

# Implementation of X, other platforms


def get_linkedin_user_details(linkedin_url: str) -> LinkedInProfileOutput:
    return LinkedInProfileOutput(
        username="pratyush_kumar_bisoyi",
        headline="Software Engineer",
        location="India",
        connections=500,
        skills=["Python", "Selenium", "Web Scraping"],
        education=["B.Tech in Computer Science"],
        postimpression=1000,
        no_of_posts=10,
        Followers_count=200,
        profile_viewers=300,
        meaningful_connections=50,
        search_appearances=100,
        posts=[
            LinkedInPost(
                content="Excited to share my latest project!",
                likes=100,
                comments=10,
                shares=5,
                tags=["Python", "WebScraping"]
            )
        ],
        profile_strength=80
    )

def get_github_user_details(github_url: str) -> GitHubUserOutput:
    return GitHubUserOutput(
        username="pratyush_kumar_bisoyi",
        repositories=[
            GitHubRepositoryOutput(
                repository_name="Awesome-Project",
                description="An awesome project that does amazing things.",
                forks=10,
                stars=50
            )
        ],
        no_of_repositories=1,
        forks_count=10,
        stars_count=50,
        viewers_count=100,
        contributions_count=5,
        email="pratyushbisoyi09@gmail.com",
        followers_count=200,
        following_count=100
    )

