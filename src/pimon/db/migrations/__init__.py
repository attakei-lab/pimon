"""Migration handler module.

Sub-modules will be migration hooks.
"""
from datetime import datetime

from .. import entities


def sync_new_tables():
    """Create all tables.

    This command is creating all tables from ``pimon.db.entities``.
    And, pin revision into Migration schema.
    """
    entities.Migration.create_table(safe=True)
    entities.Migration.create(
        revision=entities.REVISION, name="sync_all_schema", apply_at=datetime.now()
    )
