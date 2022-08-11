"""CLI endpoint for pimon."""
import sys
from pathlib import Path

import click

from .app import console
from .app.settings import ApplicationSettings
from .app.workspace import Workspace, WorkspaceError


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
    console.info("Hello pimon!!")
    try:
        workspace = Workspace(root=ctx.obj["workspace"])
        console.echo(f"Target workspace is '{workspace.root}'")
        workspace.setup()
    except (CommadError, WorkspaceError) as err:
        console.error(err)
        ctx.exit(1)
    console.info("Finished!!")


@cli.command()
@click.pass_context
def upgrade(ctx: click.Context):
    """Upgrade workspace.

    Workspace folder must be exits.
    """
    console.info("Upgrading workspace.")
    try:
        workspace = Workspace(root=ctx.obj["workspace"])
        console.echo(f"Target workspace is '{workspace.root}'")
        workspace.verify()
        workspace.migrate_db()
    except (CommadError, Exception) as err:
        console.error(err)
        ctx.exit(1)
    console.info("Finished!!")


@cli.command("accounts:add")
@click.pass_context
def add_accounts(ctx: click.Context):
    """Register new account settings.

    If you set duplicated name, prompt override.
    """
    from .app.accounts import prompt_account_settings

    console.info("Adding email account.")
    try:
        workspace = Workspace(root=ctx.obj["workspace"])
        console.echo(f"Target workspace is '{workspace.root}'")
        workspace.verify()
        settings = ApplicationSettings.load(workspace.settings_path)
        name, account_settings = prompt_account_settings()
        if name in settings.accounts:
            ans = click.confirm("Name is duplicated. Do you override it ?")
            if ans is False:
                raise CommadError("Canceled.")
        settings.accounts[name] = account_settings
        settings.save(workspace.settings_path)
    except (CommadError, Exception) as err:
        console.error(err)
        ctx.exit(1)
    console.info("Finished!!")


@cli.command()
@click.option(
    "--name",
    type=str,
    default=None,
    help="Account name in settings. if it is not set, fetch from all accounts",
)
@click.pass_context
def fetch(ctx: click.Context, name: str):
    """Fetch messages from IMAP servers registered in settings."""
    from .app.usecases.fetch_messages import Source, execute

    console.info("Adding email account.")
    try:
        workspace = Workspace(root=ctx.obj["workspace"])
        console.echo(f"Target workspace is '{workspace.root}'")
        workspace.verify()
        src = Source(
            workspace=workspace,
            settings=ApplicationSettings.load(workspace.settings_path),
            target=name,
        )
        execute(src)
    except (CommadError, WorkspaceError) as err:
        console.error(err)
        ctx.exit(1)
    console.info("Finished!!")


def main():  # noqa: D103
    cli()
