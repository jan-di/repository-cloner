"""
Command line interface
"""

import importlib.metadata
import sys
from os import path

import click
from repository_cloner.context import GlobalContext
from repository_cloner.sync import plan_target
from repository_cloner.config import read_config


@click.group()
@click.option("--config", "-c", help="Specify path to confg file")
def cli(config: str = None):
    GlobalContext.working_dir = path.realpath(".")

    if not config:
        config = path.join(GlobalContext.working_dir, "config.yaml")

    GlobalContext.config_path = config


@cli.command(name="version", help="Show the version of the application")
def cli_version():
    app_version = importlib.metadata.version("repository_cloner")

    click.echo(f"Repository Cloner: {app_version}")
    click.echo(f"Python: {sys.version}")


@cli.command(name="sync", help="Synchronize repositories")
@click.option("--yes", "-y", is_flag=True, default=False)
def cli_sync(yes: bool):
    config_file = GlobalContext.config_path
    config = read_config(config_file)

    actions = []
    for target in config.targets:
        click.echo(f"Syncing target: {target.name}")

        actions += plan_target(target)

    # Print plan
    if len(actions) == 0:
        click.echo("Nothing to do")
        return

    click.echo("Plan:")
    for action in actions:
        click.echo(f"- {action.description()}")

    if not yes:
        if not click.confirm("Do you want to continue?"):
            return

    click.echo("Executing:")
    for action in actions:
        click.echo(f"- {action.description()}")
        action.execute()


if __name__ == "__main__":
    cli()
