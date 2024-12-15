"""
Command line interface
"""

import importlib.metadata
import sys
from os import path

import click
from repository_cloner.context import GlobalContext
from repository_cloner.sync import sync


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
def cli_sync():
    sync(GlobalContext.config_path)


if __name__ == "__main__":
    cli()
