"""'Use Case' to fetch messages from IMAP servers."""
from typing import Dict, Optional

from dateutil.parser import parse as parse_datestr
from imap_tools import MailBox
from peewee import SqliteDatabase
from pydantic import BaseModel, Field

from ...db import engine
from ...db.entities import Message
from .. import console
from ..settings import AccountSettings, ApplicationSettings
from ..workspace import Workspace


class Source(BaseModel):
    """Input for this UseCase."""

    settings: ApplicationSettings
    workspace: Workspace
    target: Optional[str] = None


class Context(BaseModel):
    """Output context for this UseCase."""

    new_messages: Dict[str, int] = Field(default_factory=dict)

    def all_messages(self) -> int:
        """Calc count of all new messages."""
        return sum(self.new_messages.values())


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
        console.echo(f"Fetch from '{name}' ... ", nl=False)
        account = src.settings.accounts[name]
        created = work_in_mailbox(name, account)
        console.info(f"{created} messages added.")
        ctx.new_messages[name] = created

    return ctx


def work_in_mailbox(name: str, settings: AccountSettings) -> int:
    """Sub-proc per mailbox."""
    cnt = 0
    with MailBox(settings.host, settings.port).login(
        settings.username, settings.password, settings.inbox
    ) as mb:
        for msg in mb.fetch(mark_seen=False, headers_only=True):
            content = {
                "account": name,
                "uid": msg.uid,
                "sender": msg.from_values.full,
                "subject": msg.subject,
                "received_at": parse_datestr(msg.date_str),
            }
            msg, created = Message.get_or_create(**content)
            if created:
                cnt += 1
    return cnt
