"""'Use Case' to fetch messages from IMAP servers."""
from dataclasses import dataclass
from typing import Dict, Optional

from dateutil.parser import parse as parse_datestr
from imap_tools import MailBox
from peewee import SqliteDatabase
from pydantic import BaseModel, Field

from ... import console
from ...db import engine
from ...db.entities import Message
from ...settings import AccountSettings
from .. import models
from . import BaseSource


@dataclass
class Source(BaseSource):
    """Input for this UseCase."""

    target: Optional[str] = None


class FetchResult(BaseModel):
    """Context class for fetching per account."""

    class Config:  # noqa: D106
        arbitrary_types_allowed = True

    name: str
    added: int = 0
    error: Optional[Exception] = None

    def out_console(self) -> str:
        """Output text for terminal environment."""
        console.echo(f"Fetch from '{self.name}': ", nl=False)
        if self.error:
            console.error(f"FAILED - {self.error}")
        else:
            console.info(f"SUCCEED - {self.added} messages added")


class Context(BaseModel):
    """Output context for this UseCase."""

    accounts: Dict[str, FetchResult] = Field(default_factory=dict)


def execute(src: Source) -> Context:
    """Run logic for this UseCase."""
    targets = []
    if src.target:
        targets.append(src.target)
    else:
        targets += src.settings.accounts.keys()

    ctx = Context()
    engine.initialize(SqliteDatabase(src.workspace.db_path))
    for name in targets:
        account = src.settings.accounts[name]
        result = work_in_mailbox(name, account)
        result.out_console()
        ctx.accounts[name] = result

    return ctx


def work_in_mailbox(name: str, settings: AccountSettings) -> FetchResult:
    """Sub-proc per mailbox."""
    result = FetchResult(name=name)
    try:
        with MailBox(settings.host, settings.port).login(
            settings.username, settings.password, settings.inbox
        ) as mb:
            for msg in mb.fetch(mark_seen=False, headers_only=True):
                model = models.Message(
                    account=name,
                    uid=msg.uid,
                    sender=msg.from_values.full,
                    subject=msg.subject,
                    received_at=parse_datestr(msg.date_str),
                )
                msg, created = Message.get_or_create(**model.dict())
                if created:
                    result.added += 1
    except Exception as err:
        result.error = err
    return result
