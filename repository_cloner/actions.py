from abc import ABC, abstractmethod
import os
from os import path

from git import Repo as GitRepo

from repository_cloner.cloner import Repository


class BaseAction(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def description(self):
        pass


class CloneRepositoryAction(BaseAction):
    def __init__(
        self,
        remote_repository: Repository,
    ):
        self.remote_repository = remote_repository
        super().__init__()

    def execute(self):
        full_path = self.__get_target_path()
        os.makedirs(full_path, exist_ok=True)

        git_repo = GitRepo.clone_from(self.remote_repository.clone_url, full_path)
        with git_repo.config_writer() as config:
            config.set_value(
                "jan-di.repository-cloner", "uid", self.remote_repository.uid
            )

    def description(self):
        return f"Clone {self.remote_repository} to {self.__get_target_path()}"

    def __get_target_path(self):
        return path.join(
            self.remote_repository.base_path, self.remote_repository.rel_path
        )


class DeleteRepositoryAction(BaseAction):
    def __init__(
        self,
        local_repository: Repository,
    ):
        self.local_repository = local_repository
        super().__init__()

    def execute(self):
        print("Delete stub")
        # TODO: Implement

    def description(self):
        return f"Delete {self.local_repository} at {self.__get_local_path()}"

    def __get_local_path(self):
        return path.join(
            self.local_repository.base_path, self.local_repository.rel_path
        )


class TrashRepositoryAction(BaseAction):
    def __init__(
        self,
        local_repository: Repository,
    ):
        self.local_repository = local_repository
        super().__init__()

    def execute(self):
        print("Trash stub")
        # TODO: Implement

    def description(self):
        return f"Trash {self.local_repository} at {self.__get_local_path()}"

    def __get_local_path(self):
        return path.join(
            self.local_repository.base_path, self.local_repository.rel_path
        )


class MoveRepositoryAction(BaseAction):
    def __init__(
        self,
        local_repository: Repository,
        remote_repository: Repository,
    ):
        self.local_repository = local_repository
        self.remote_repository = remote_repository
        super().__init__()

    def execute(self):
        print("Trash stub")
        # TODO: Implement

    def description(self):
        return f"Moving {self.local_repository} to {self.remote_repository}"
