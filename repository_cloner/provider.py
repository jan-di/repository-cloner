from github import Github, Auth
from repository_cloner.config import Target, GithubConfig
from repository_cloner.cloner import Repository


def get_provider(target: Target):
    match target.type:
        case "github":
            return GithubProvider(target.name, target.basePath, target.github)


class GithubProvider:
    def __init__(
        self, target_name: str, base_path: str, github_config: GithubConfig
    ) -> None:
        auth = Auth.Token(github_config.apiToken)
        self.target_name = target_name
        self.base_path = base_path
        self.github_api = Github(base_url=github_config.apiUrl, auth=auth)
        self.strategy = github_config.syncStrategy
        self.ignore_archived = github_config.ignoreArchived

    def list_repositories(self) -> dict[str, Repository]:
        if self.strategy == "Owned":
            github_repos = list(self.github_api.get_user().get_repos())
        else:
            raise ValueError("Unknown strategy")
        repositories = {}

        for github_repo in github_repos:
            repo_id = str(github_repo.id)

            if self.ignore_archived and github_repo.archived:
                continue

            repositories[repo_id] = Repository(
                uid=repo_id,
                target_name=self.target_name,
                base_path=self.base_path,
                rel_path=github_repo.full_name.lower(),
                clone_url=github_repo.ssh_url,
            )

        return repositories
