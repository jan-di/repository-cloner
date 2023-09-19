import os
from os import path
from git import Repo as GitRepo

from src.config import Config, Target


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
        return f"{self.target_name}/{self.uid} {self.clone_url} -> {self.base_path}/{self.rel_path}"


class Cloner:
    def __init__(self, config: Config) -> None:
        self.config = config

    def clone_repository(self, repository: Repository):
        full_path = path.join(repository.base_path, repository.rel_path)
        os.makedirs(full_path, exist_ok=True)

        git_repo = GitRepo.clone_from(repository.clone_url, full_path)
        with git_repo.config_writer() as config:
            config.set_value("jan-di.repository-cloner", "uid", repository.uid)

    def list_local_repositories(self, target: Target):
        repositories = []
        for root, dirs, _files in os.walk(target.basePath):
            if ".git" in dirs:
                repo_dir = path.relpath(root, target.basePath)
                dirs.remove(".git")  # do not traverse further into .git folders
                repositories.append(
                    self.read_repository(
                        base_path=target.basePath,
                        rel_path=repo_dir,
                        target_name=target.name,
                    )
                )

        return repositories

    def read_repository(self, base_path: str, rel_path: str, target_name: str):
        full_path = path.join(base_path, rel_path)
        git_repo = GitRepo(full_path)
        with git_repo.config_writer() as config:
            uid = config.get_value("jan-di.repository-cloner", "uid")
            remote = git_repo.remote().url

            return Repository(
                uid=uid,
                target_name=target_name,
                clone_url=remote,
                base_path=base_path,
                rel_path=rel_path,
            )
