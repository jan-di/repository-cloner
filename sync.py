import os

from src.config import read_config
from src.provider import get_provider
from src.cloner import Cloner

script_dir = os.path.dirname(os.path.realpath(__file__))
config = read_config(f"{script_dir}/config.yaml")
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
