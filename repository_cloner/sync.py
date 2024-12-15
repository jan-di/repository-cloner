import click

from repository_cloner.config import read_config
from repository_cloner.provider import get_provider
from repository_cloner.cloner import Cloner
from repository_cloner.actions import (
    CloneRepositoryAction,
    DeleteRepositoryAction,
    MoveRepositoryAction,
    TrashRepositoryAction,
)


def sync(config_file: str):
    config = read_config(config_file)
    cloner = Cloner(config)

    for target in config.targets:
        # Read local repositories
        local_repositories = cloner.list_local_repositories(target)

        # Read remote repositories
        provider = get_provider(target)
        remote_repositories = provider.list_repositories()

        # print("=== local")
        # for r in local_repositories.values():
        #     print(r)

        # print("=== remote")
        # for r in remote_repositories.values():
        #     print(r)

        actions = []

        local_ids = set(local_repositories.keys())
        remote_ids = set(remote_repositories.keys())

        # Check for repositories that not exists on remote (anymore)
        local_only_ids = local_ids - remote_ids
        local_only_repositories = [local_repositories[rid] for rid in local_only_ids]

        for repo in local_only_repositories:
            move_to_trash = False
            if move_to_trash:
                actions.append(TrashRepositoryAction(repo))
            else:
                actions.append(DeleteRepositoryAction(repo))
        # Check for repositories that only exists on remote
        remote_only_ids = remote_ids - local_ids
        remote_only_repositories = [remote_repositories[rid] for rid in remote_only_ids]

        for repo in remote_only_repositories:
            actions.append(CloneRepositoryAction(repo))

        # Check for repositories that exists on both local and remote
        common_ids = local_ids & remote_ids
        for common_id in common_ids:
            local_repo = local_repositories[common_id]
            remote_repo = remote_repositories[common_id]

            if local_repo.rel_path != remote_repo.rel_path:
                actions.append(MoveRepositoryAction(local_repo, remote_repo))

        # Print plan
        click.echo("Plan:")
        for action in actions:
            click.echo(f"- {action.description()}")

        # TODO: Check for dry run or a -y flag here
        # for action in actions:
        #     action.execute()
