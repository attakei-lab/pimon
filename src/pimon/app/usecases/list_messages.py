"""UseCase to display list of messages."""
import shutil
from dataclasses import dataclass, field
from typing import List

from peewee import SqliteDatabase

from ... import console
from ...db import engine
from ...db.entities import Message
from . import BaseSource

SUBJECT_MAX_LENGTH = 50


Source = BaseSource


@dataclass
class Context:  # noqa: D101
    messages: List[Message] = field(default_factory=list)
    line_size: int = 0
    account_max_length: int = 0
    uid_max_length: int = 0


def execute(src: Source):
    """Run logic for this UseCase."""
    engine.initialize(SqliteDatabase(src.workspace.db_path))
    ctx = Context(line_size=shutil.get_terminal_size()[0])
    for msg in Message.select():
        ctx.messages.append(msg)
        ctx.account_max_length = max([len(msg.account), ctx.account_max_length])
        ctx.uid_max_length = max([len(str(msg.uid)), ctx.uid_max_length])
    message_length = (
        (ctx.line_size - ctx.account_max_length - ctx.uid_max_length - 2) // 5 * 2
    )
    for msg in ctx.messages:
        account = msg.account + " " * (ctx.account_max_length - len(msg.account) + 1)
        uid = str(msg.uid) + " " * (ctx.uid_max_length - len(str(msg.uid)) + 1)
        subject = (
            msg.subject
            if len(msg.subject) <= message_length
            else msg.subject[: message_length + 4] + " ..."
        )
        console.echo(f"{account}{uid}{subject}")
