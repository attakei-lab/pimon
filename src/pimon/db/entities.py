import peewee

from . import engine


class Message(peewee.Model):
    """Message data that manage in pimon."""

    account = peewee.CharField()
    uid = peewee.IntegerField()
    sender = peewee.CharField()
    subject = peewee.CharField()
    received_at = peewee.DateTimeField()

    class Meta:  # noqa: D106
        database = engine
        primary_key = peewee.CompositeKey("account", "uid")
