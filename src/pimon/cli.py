"""CLI endpoint for pimon."""
import sys
from pathlib import Path

import click

from .db import migrations


class CommadError(Exception):  # noqa: D101
    pass


class Console:
    """Click echo proc wrapper."""

    @classmethod
    def _out(cls, text: str, fg: str, nl: bool = True):  # noqa: D102
        click.echo(click.style(text, fg=fg), nl=nl)

    @classmethod
    def echo(cls, msg: str, nl: bool = True):  # noqa: D102
        click.echo(msg, nl=nl)

    @classmethod
    def info(cls, msg: str, nl: bool = True):  # noqa: D102
        cls._out(msg, "green", nl=nl)

    @classmethod
    def warning(cls, msg: str, nl: bool = True):  # noqa: D102
        cls._out(msg, "yellow", nl=nl)

    @classmethod
    def error(cls, msg: str, nl: bool = True):  # noqa: D102
        cls._out(msg, "red", nl=nl)


def resolve_workspace() -> Path:
    """Build user-based workspace automately."""
    if sys.platform in ("linux", "linux2"):
        return Path.home() / ".config" / "pimon"
    raise Exception(f"{sys.platform} is not supported now")


@click.group()
@click.option(
    "-ws",
    "--workspace",
    type=click.Path(
        file_okay=False,
        dir_okay=True,
        resolve_path=True,
        path_type=Path,
    ),
    default=None,
    help="Worspace folder to management options and data",
)
@click.pass_context
def cli(ctx: click.Context, workspace: Path = None):  # noqa: D103
    ctx.ensure_object(dict)
    if not workspace:
        workspace = resolve_workspace()
    ctx.obj["workspace"] = workspace


@cli.command()
@click.pass_context
def init(ctx: click.Context):
    """Initialize workspace.

    Workspace folder must be not exists.
    """
    Console.info("Hello pimon!!")
    try:
        workspace: Path = ctx.obj["workspace"]
        Console.echo(f"Target workspace is '{workspace}'")
        if workspace.exists():
            raise CommadError(
                "Workspace is already exists. "
                "Please specify other path or delete target"
            )
            ctx.exit(1)
        workspace.mkdir(parents=True)
        Console.echo("Create database ... ", nl=False)
        db_path = workspace / "db.sqlite"
        migrations.MigrationContext.new(db_path).migrate()
        Console.info("OK")
    except (CommadError, Exception) as err:
        Console.error(err)
        ctx.exit(1)
    Console.info("Finished!!")


@cli.command()
@click.pass_context
def upgrade(ctx: click.Context):
    """Upgrade workspace.

    Workspace folder must be exits.
    """
    Console.info("Upgrading workspace.")
    workspace: Path = ctx.obj["workspace"]
    if not workspace.exists():
        Console.error("Workspace is not exists")
        ctx.exit(1)
    try:
        Console.echo("Migrate database ... ", nl=False)
        db_path = workspace / "db.sqlite"
        migrations.MigrationContext.new(db_path).migrate()
        Console.info("OK")
    except (CommadError, Exception) as err:
        Console.error(err)
        ctx.exit(1)
    Console.info("Finished!!")


def main():  # noqa: D103
    cli()
