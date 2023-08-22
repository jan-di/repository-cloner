
import os

from src.config import read_config
from src.provider import GithubProvider

script_dir = os.path.dirname(os.path.realpath(__file__))
config = read_config(f"{script_dir}/config.yaml")

for target in config.targets:
    match target.type:
        case "github":
            provider = GithubProvider(target.github)

    repositories = provider.list_repositories()

    for r in repositories:
        print(f"- {r.uid}|{r.name}|{r.path}|{r.clone_url}")
