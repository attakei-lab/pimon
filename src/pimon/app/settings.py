"""Definition of settings to behavoirs."""
from pathlib import Path

from pydantic import BaseSettings


class ApplicationSettings(BaseSettings):
    """All application settings.

    This class must be loaded from ``settings.json`` in workspace.
    """


def create_new_settings(save_to: Path) -> ApplicationSettings:
    """Generate and save new settings file.

    Settings has default values.
    """
    settings = ApplicationSettings()
    save_to.write_text(settings.json())
