import os
from os import path
from git import Repo as GitRepo

from repository_cloner.config import Target


class Repository:
    def __init__(
        self,
        uid: str,
        target_name: str,
        clone_url: str,
        base_path: str,
        rel_path: str,
    ) -> None:
        self.uid = uid
        self.target_name = target_name
        self.clone_url = clone_url
        self.base_path = base_path
        self.rel_path = rel_path

    def __str__(self):
        return f"{self.target_name}:{self.rel_path}"


class Cloner:
    def list_local_repositories(self, target: Target) -> dict[str, Repository]:
        repositories = {}
        for root, dirs, _files in os.walk(target.basePath):
            if ".git" in dirs:
                repo_dir = path.relpath(root, target.basePath)
                dirs.remove(".git")  # do not traverse further into .git folders
                repo = self.read_repository(
                    base_path=target.basePath,
                    rel_path=repo_dir,
                    target_name=target.name,
                )
                repositories[repo.uid] = repo

        return repositories

    def read_repository(
        self, base_path: str, rel_path: str, target_name: str
    ) -> Repository:
        full_path = path.join(base_path, rel_path)
        git_repo = GitRepo(full_path)
        with git_repo.config_writer() as config:
            uid = str(config.get_value("jan-di.repository-cloner", "uid"))
            remote = git_repo.remote().url

            return Repository(
                uid=uid,
                target_name=target_name,
                clone_url=remote,
                base_path=base_path,
                rel_path=rel_path,
            )
