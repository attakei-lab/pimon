"""Account managemnt."""
from typing import Tuple

import click

from ..settings import AccountSettings, RemoveSettings


def prompt_account_settings() -> Tuple[str, AccountSettings]:
    """Prompt and generate account-settings."""
    # Propmpt settings
    name = click.prompt("Name in settings", type=str)
    host = click.prompt("Host", type=str)
    port = click.prompt("Port", type=int)
    username = click.prompt("Username", type=str)
    password = click.prompt("Password", type=str, hide_input=True)
    inbox = click.prompt("Inbox name", type=str, default="INBOX")
    remove_proc = click.prompt(
        "Archive process", type=click.Choice(["delete", "move"]), show_choices=True
    )
    remove_move_to = (
        click.prompt("Move to remove", type=str) if remove_proc == "move" else None
    )

    # Generate
    remove = RemoveSettings(proc=remove_proc)
    if remove.proc == "move":
        remove.options["dist"] = remove_move_to
    settings = AccountSettings(
        host=host,
        port=port,
        username=username,
        password=password,
        inbox=inbox,
        remove=remove,
    )
    return name, settings
