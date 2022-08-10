"""For ``pimon.db.migrations``."""
import peewee

from pimon.db import engine, entities, migrations


def test__work__sync_new_tables():  # noqa: D103
    db = peewee.SqliteDatabase(":memory:")
    engine.initialize(db)
    migrations.sync_new_tables()
    assert db.table_exists(entities.Migration._meta.name)
    assert db.table_exists(entities.Message._meta.name)
