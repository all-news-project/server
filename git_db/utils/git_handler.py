import os
from git import Repo, GitCommandError
from git_db.utils.consts import RepoConsts
from logger import get_current_logger


class GitHandler:
    def __init__(self):
        self.logger = get_current_logger()

    def clone_repo_if_needed(self):
        self.logger.debug("get_repo_if_needed")
        if not os.path.exists(RepoConsts.REPO_PATH):
            self.logger.warning(f"folder `{RepoConsts.REPO_PATH}` not exists")
            self.logger.debug(f"Cloning repo: `{RepoConsts.REPO_URL}` with depth of {RepoConsts.DEPTH}...")
            Repo.clone_from(RepoConsts.REPO_URL, RepoConsts.REPO_PATH, depth=RepoConsts.DEPTH)
            self.logger.info(f"Cloned repo to `{RepoConsts.REPO_PATH}`")

    def update_repo(self):
        self.logger.debug("update_exists_repo")
        repo = Repo(RepoConsts.REPO_PATH)
        origin = repo.remotes.origin
        origin.pull()

    def save_repo(self, commit: str):
        self.logger.debug("save_repo")
        repo = Repo(RepoConsts.REPO_PATH)
        origin = repo.remote(name='origin')
        existing_branch = repo.heads['main']
        existing_branch.checkout()
        try:
            repo.git.add('--all')
            repo.index.commit(commit)
            self.logger.info(f'Done committing with commit: `{commit}`')
        except GitCommandError as e:
            self.logger.debug(str(e))
            if "your branch is ahead of" in str(e).lower():
                self.logger.warning("No commit needed")
        try:
            origin.push()
        except GitCommandError as e:
            self.logger.error(str(e))
