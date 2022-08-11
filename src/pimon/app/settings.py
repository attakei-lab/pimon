"""Definition of settings to behavoirs."""
from pathlib import Path

import tomli
import tomli_w
from pydantic import BaseSettings


class ApplicationSettings(BaseSettings):
    """All application settings.

    This class must be loaded from ``settings.json`` in workspace.
    """

    @classmethod
    def load(cls, src_path: Path) -> "ApplicationSettings":
        """Load settings from TOML-file."""
        obj = tomli.loads(src_path.read_text())
        return cls.from_orm(obj)

    def save(self, dst: Path):
        """Save settings as TOML-file."""
        dst.write_text(tomli_w.dumps(self.dict()))


def create_new_settings(save_to: Path) -> ApplicationSettings:
    """Generate and save new settings file.

    Settings has default values.
    """
    settings = ApplicationSettings()
    settings.save(save_to)
