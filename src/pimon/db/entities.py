import peewee

from . import engine

REVISION = 2


class Base(peewee.Model):  # noqa: D101
    class Meta:  # noqa: D106
        database = engine


class Migration(Base):
    """For schema management."""

    revision = peewee.IntegerField(primary_key=True)
    name = peewee.CharField()
    apply_at = peewee.DateTimeField()


class Message(Base):
    """Message data that manage in pimon."""

    account = peewee.CharField()
    uid = peewee.IntegerField()
    sender = peewee.CharField()
    subject = peewee.CharField()
    received_at = peewee.DateTimeField()

    class Meta:  # noqa: D106
        database = engine
        primary_key = peewee.CompositeKey("account", "uid")
