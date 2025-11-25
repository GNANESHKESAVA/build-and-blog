import git
from git.exc import InvalidGitRepositoryError

class GitHandler:
    def __init__(self, repo_path="."):
        try:
            self.repo = git.Repo(repo_path, search_parent_directories=True)
        except InvalidGitRepositoryError:
            self.repo = None

    def is_valid_repo(self):
        return self.repo is not None

    def get_staged_diff(self):
        if not self.repo:
            return ""
        return self.repo.git.diff("--staged")

    def has_unstaged_changes(self):
        if not self.repo:
            return False
        return self.repo.is_dirty(untracked_files=True)

    def get_commit_history(self, branch="main"):
        if not self.repo:
            return []
        # This is a simplified version, might need adjustment based on actual needs
        try:
            commits = list(self.repo.iter_commits(f"{branch}..HEAD"))
            return commits
        except git.exc.GitCommandError:
            return []

    def push_branch(self, branch_name):
        if not self.repo:
            return False
        try:
            # Check if we have a token to use for auth
            import os
            token = os.getenv("GITHUB_TOKEN")
            origin = self.repo.remote(name='origin')
            
            if token and "github.com" in origin.url and "https" in origin.url:
                # Construct authenticated URL: https://TOKEN@github.com/user/repo.git
                auth_url = origin.url.replace("https://", f"https://{token}@")
                # Push using the new URL
                self.repo.git.push(auth_url, branch_name)
            else:
                # Fallback to standard push (might fail in Docker without creds)
                origin.push(branch_name)
            
            return True
        except Exception as e:
            print(f"Error pushing branch: {e}")
            return False
