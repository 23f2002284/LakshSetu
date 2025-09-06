from User_Processing_node import GitHubRepositoryOutput, GitHubUserOutput, LinkedInProfileOutput
from typing import List, Optional


def build_github_user_output_from_analysis(analysis: dict) -> GitHubUserOutput:
    """Build a GitHubUserOutput object from a GitHub Profile Analysis dict.

    Expected input shape (keys):
    - profile: { login, name, bio, company, location, blog, twitter, public_repos, followers_count, following_count }
    - repos: [ { name, description, stars, primary_language, url, last_updated, forks? } ]
    - followers: [ ... ]
    - following: [ ... ]
    - contributions: [ ... ]

    Notes:
    - Email is not present in the analysis; we set it to an empty string.
    - Company in the model is a list; we convert a single value to a 1-item list.
    - Forks may be missing per repo; default to 0.
    """
    p = (analysis or {}).get("profile", {}) or {}
    repos = (analysis or {}).get("repos", []) or []
    followers = (analysis or {}).get("followers", []) or []
    following = (analysis or {}).get("following", []) or []
    contributions = (analysis or {}).get("contributions", []) or []

    repo_objs: List[GitHubRepositoryOutput] = []
    stars_total = 0
    forks_total = 0
    viewers_total = 0  # Not provided in the analysis; keep 0

    for r in repos:
        stars = r.get("stars") or 0
        forks = r.get("forks") or 0
        repo_objs.append(
            GitHubRepositoryOutput(
                repository_name=r.get("name", ""),
                description=(r.get("description") or "").strip(),
                forks=forks,
                stars=stars,
                url=r.get("url", ""),
                last_updated=r.get("last_updated", ""),
            )
        )
        stars_total += stars
        forks_total += forks

    username = p.get("login") or ""
    bio = p.get("bio")
    email = p.get("email") or ""
    company_val = p.get("company")
    company_list = [company_val] if company_val else []
    location = p.get("location")
    blog = (p.get("blog") or None) or None
    twitter = p.get("twitter")

    followers_count = p.get("followers_count")
    if followers_count is None:
        followers_count = len(followers)

    following_count = p.get("following_count")
    if following_count is None:
        following_count = len(following)

    return GitHubUserOutput(
        username=username,
        bio=bio,
        email=email,
        company=company_list,
        location=location,
        blog=blog if blog else None,
        repositories=repo_objs,
        no_of_repositories=len(repos),
        forks_count=forks_total,
        stars_count=stars_total,
        viewers_count=viewers_total,
        contributions_count=len(contributions),
        followers_count=followers_count,
        following_count=following_count,
        twitter=twitter,
    )


linked_in_profile_parser = {
    "username": "Biswajit Polai", 
    "email": "biswajitpolai5@gmail.com", 
    "headline": "CSE Undergrad", 
    "location": "Brahmapur, Odisha, India", 
    "skills": [], 
    "education": [{
        "Colleges": [
            {"name": "Biju Patnaik University of Technology, Odisha", "degree": "Bachelor of Technology", "field_of_study": "Computer Science", "CGPA": None, "start_year": 2023, "end_year": 2027}, 
            {"name": "Parala Maharaja Engineering College, Berhampur", "degree": "Bachelor of Technology", "field_of_study": "Computer Science", "CGPA": None, "start_year": 2024, "end_year": 2027}, 
            {"name": "Parala Maharaja Engineering College, Berhampur", "degree": "Bachelor of Technology", "field_of_study": "Electronics and Telecommunication Engineering", "CGPA": None, "start_year": 2023, "end_year": 2024}
        ],
        "Schools": [
            {"name": "De Paul School,Berhampur", "class_name": "XII", "subjects_taken": "PCMB", "Marks": None, "start_year": 2020, "end_year": 2022}, 
            {"name": "De Paul School,Berhampur", "class_name": "X", "subjects_taken": None, "Marks": None, "start_year": 2019, "end_year": 2020}
        ]
    }], 
    "Certifications": ["Big Data Modeling and Management Systems", "Data Analytics in Python", "ABV-IIITM Credentials", "IIT BBS credentials", "Python for Data science"], 
    "Honorsawards": ["Runner\'s up at Hack For Tomorrow Grand Finale"]
}
linked_in_user_output = build_github_user_output_from_analysis(linked_in_profile_parser)


github_profile_analysis = {
  "profile": {
    "login": "biswajitpolai",
    "name": "Biswajit Polai",
    "bio": "Intern @ ABV-IIITM Gwalior '25 \u2022 Intern @ IIT BBS '25",
    "company": None,
    "location": "Berhampur,odisha ,India",
    "blog": "",
    "twitter": None,
    "public_repos": 11,
    "followers_count": 2,
    "following_count": 0
  },
  "repos": [
    {
      "name": "summer_project_2025",
      "description": "stuffs related to summer 2025",
      "stars": 0,
      "primary_language": None,
      "url": "https://github.com/biswajitpolai/summer_project_2025",
      "last_updated": "2025-06-08T04:52:34Z"
    },
    {
      "name": "credit_card_fraud",
      "description": "This project leverages machine learning techniques to identify fraudulent credit card transactions in a dataset. ",
      "stars": 0,
      "primary_language": "Jupyter Notebook",
      "url": "https://github.com/biswajitpolai/credit_card_fraud",
      "last_updated": "2025-06-03T15:33:17Z"
    },
    {
      "name": "trees-and-beyond",
      "description": "stuffs related to non linear data structure and beyond..",
      "stars": 0,
      "primary_language": "Java",
      "url": "https://github.com/biswajitpolai/trees-and-beyond",
      "last_updated": "2025-04-29T06:49:49Z"
    },
    {
      "name": "Millet_recommender",
      "description": "No description provided.",
      "stars": 1,
      "primary_language": "Java",
      "url": "https://github.com/biswajitpolai/Millet_recommender",
      "last_updated": "2025-03-27T16:50:25Z"
    },
    {
      "name": "Feme_Vision",
      "description": "The Women Safety Analytics system leverages advanced surveillance and analytical solutions for real-time threat detection.",
      "stars": 0,
      "primary_language": "Python",
      "url": "https://github.com/biswajitpolai/Feme_Vision",
      "last_updated": "2025-02-28T17:23:26Z"
    },
    {
      "name": "AilmentArchivist",
      "description": "No description provided.",
      "stars": 0,
      "primary_language": "Java",
      "url": "https://github.com/biswajitpolai/AilmentArchivist",
      "last_updated": "2025-02-12T05:57:41Z"
    },
    {
      "name": "Retail_Customer_Segmentation",
      "description": "No description provided.",
      "stars": 0,
      "primary_language": "Jupyter Notebook",
      "url": "https://github.com/biswajitpolai/Retail_Customer_Segmentation",
      "last_updated": "2024-10-28T11:43:38Z"
    },
    {
      "name": "WageDisparityInsights",
      "description": "Salary Disparities Between Men and Women Project Overview ",
      "stars": 0,
      "primary_language": "Jupyter Notebook",
      "url": "https://github.com/biswajitpolai/WageDisparityInsights",
      "last_updated": "2024-10-25T04:15:33Z"
    }
  ],
  "followers": [
    "Roshan0025",
    "Seikh05"
  ],
  "following": [],
  "contributions": []
}
github_user_output = build_github_user_output_from_analysis(github_profile_analysis)