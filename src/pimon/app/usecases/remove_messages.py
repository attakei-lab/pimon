"""'Use Case' to remove messages from IMAP servers and database."""
from dataclasses import dataclass
from typing import Optional

from imap_tools import MailBox
from peewee import SqliteDatabase
from pydantic import BaseModel

from ...db import engine
from ...db.entities import Message
from .. import console
from ..settings import ApplicationSettings
from ..workspace import Workspace


class Source(BaseModel):
    """Input for this UseCase."""

    settings: ApplicationSettings
    workspace: Workspace
    account: str
    uid: int


@dataclass
class Result:
    """For handle by cli proc."""

    err: Optional[Exception] = None


def execute(src: Source) -> Result:
    """Run logic for this UseCase."""
    engine.initialize(SqliteDatabase(src.workspace.db_path))
    # Find message
    msg: Optional[Message] = Message.get_or_none(account=src.account, uid=src.uid)
    if msg is None:
        return Result(
            err=Exception(f"Message is not found (account={src.account} uid={src.uid})")
        )
    # Trash
    account = src.settings.accounts[src.account]
    try:
        with MailBox(account.host, account.port).login(
            account.username, account.password, account.inbox
        ) as mb:
            if account.remove.proc == "move":
                mb.move([str(src.uid)], account.remove.options["dist"])
            elif account.remove.proc == "delete":
                mb.delete([str(src.uid)])
        msg.delete_instance()
    except Exception as err:
        return Result(err=err)
    console.warning(f"Message is not found (account={src.account} uid={src.uid})")
    return Result()
