import peewee

from . import engine

REVISION = 1


class Base(peewee.Model):  # noqa: D101
    class Meta:  # noqa: D106
        database = engine


class Migration(Base):
    """For schema management."""

    revision = peewee.IntegerField(primary_key=True)
    name = peewee.CharField()
    apply_at = peewee.DateTimeField()
