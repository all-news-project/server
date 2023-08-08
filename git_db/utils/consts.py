import os


class RepoConsts:
    DEPTH = int(os.getenv(key="DEPTH", default=1))
    USERNAME = os.getenv(key="USERNAME")
    PASSWORD = os.getenv(key="PASSWORD")
    REPO_NAME = "api-data"
    REPO_URL = f"https://{USERNAME}:{PASSWORD}@github.com/all-news-project/{REPO_NAME}.git"
    REPO_PATH = os.getenv(key="REPO_PATH", default=f"/home/user/allnews/server/git_db/{REPO_NAME}")
    REPO_CURRENT_BRANCH = "main"
    REPO_CURRENT_REMOTE = "origin"
