"""Migration handler module.

Sub-modules will be migration hooks.
"""
from dataclasses import dataclass
from pathlib import Path

from peewee_migrate import MIGRATE_TABLE, Router
from peewee_migrate.cli import get_router

from .. import entities


@dataclass
class MigrationContext:
    """Bridge class to work likely ``peewee_migrate.cli``."""

    directory: Path
    database: Path
    history: str = MIGRATE_TABLE
    verbose: bool = False
    source: str = entities.__name__

    @classmethod
    def new(cls, db_path: Path):
        """Create by target database and ``pimon`` itself.

        :params db_path: Target database path
        """
        return cls(
            database=db_path,
            directory=Path(__file__).parent,
        )

    def get_router(self) -> Router:
        """Create ``peewee_migrate.Router`` by itself."""
        db_url = f"sqlite:///{self.database}"
        return get_router(self.directory, db_url, MIGRATE_TABLE, self.verbose)

    def create(self, name: str = None):
        """Emulate of ``peewee_migrate.cli.create``."""
        self.get_router().create(name or "auto", auto=self.source)

    def migrate(self, name: str = None):
        """Emulate of ``peewee_migrate.cli.migrate``."""
        self.get_router().run(name)
