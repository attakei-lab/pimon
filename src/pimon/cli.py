"""CLI endpoint for pimon."""
import sys
from pathlib import Path

import click


class CommadError(Exception):  # noqa: D101
    pass


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
    click.echo(click.style("Hello pimon!!", fg="green"))
    try:
        workspace: Path = ctx.obj["workspace"]
        click.echo(f"Target workspace is '{workspace}'")
        if workspace.exists():
            raise CommadError(
                "Workspace is already exists. "
                "Please specify other path or delete target"
            )
            ctx.exit(1)
        workspace.mkdir(parents=True)
    except (CommadError, Exception) as err:
        click.echo(click.style(err, fg="red"))
        ctx.exit(1)


def main():  # noqa: D103
    cli()
