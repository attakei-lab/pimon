"""Define behaviors in workspace directory."""
from dataclasses import dataclass
from functools import cached_property
from pathlib import Path

from ..db.migrations import MigrationContext
from . import console
from .settings import create_new_settings


class WorkspaceError(Exception):  # noqa: D101
    pass


@dataclass
class Workspace:
    """Application workspace for Pimon CLI."""

    root: Path

    @cached_property
    def settings_path(self) -> Path:  # noqa: D102
        return self.root / "settings.toml"

    @cached_property
    def db_path(self) -> Path:  # noqa: D102
        return self.root / "db.sqlite"

    @cached_property
    def logs_dir(self) -> Path:  # noqa: D102
        return self.root / "logs"

    def setup(self):
        """Create new workspace."""
        # Validate root
        if not self.root.exists():
            self.root.mkdir(parents=True)
        elif self.root.is_file():
            raise WorkspaceError("To setup, workspace directory must be empty.")
        for _ in self.root.glob("*"):
            raise WorkspaceError("To setup, workspace directory must be empty.")
        # Generate files
        self.migrate_db()
        console.echo("Create settings ...", nl=False)
        create_new_settings(self.settings_path)
        console.info("OK")
        console.echo("Create log directory ...", nl=False)
        self.logs_dir.mkdir()
        console.info("OK")

    def verify(self):
        """Validate file structure of workspace."""
        if not self.db_path.exists():
            raise WorkspaceError("Database is not exists in workspace.")
        if not self.settings_path.exists():
            raise WorkspaceError("Settings is not exists in workspace.")
        if not self.logs_dir.exists():
            raise WorkspaceError("Log directory is not exists in workspace.")
        return

    def migrate_db(self):
        """Generate and migrate database in workspace."""
        if self.db_path.exists():
            console.echo("Migrate database ... ", nl=False)
        else:
            console.echo("Create database ... ", nl=False)
        ctx = MigrationContext.new(self.db_path)
        ctx.migrate()
        console.info("OK")
