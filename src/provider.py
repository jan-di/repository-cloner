from github import Github, Auth
from src.config import GithubConfig
from src.repo import Repository

class GithubProvider:
    def __init__(self, github_config: GithubConfig) -> None:
        auth = Auth.Token(github_config.apiToken)
        self.github_api = Github(base_url=github_config.apiUrl, auth=auth)
        self.strategy = github_config.syncStrategy

    def list_repositories(self) -> list:
        if self.strategy == "Owned":
            github_repos = list(self.github_api.get_user().get_repos())
        repositories = []

        for github_repo in github_repos:
            repositories.append(Repository(
                uid=str(github_repo.id),
                name=github_repo.name.lower(),
                path=github_repo.full_name.lower(),
                clone_url=github_repo.clone_url
            ))

        return repositories