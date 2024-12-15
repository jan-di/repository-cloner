from repository_cloner.config import read_config
from repository_cloner.provider import get_provider
from repository_cloner.cloner import Cloner

def sync(config_file: str):
    config = read_config(config_file)
    cloner = Cloner(config)

    for target in config.targets:
        # Read local repositories
        local_repositories = cloner.list_local_repositories(target)

        # Read remote repositories
        provider = get_provider(target)
        remote_repositories = provider.list_repositories()

        print("local")
        for r in local_repositories:
            print(r)

        print("remote")
        for r in remote_repositories:
            print(r)
