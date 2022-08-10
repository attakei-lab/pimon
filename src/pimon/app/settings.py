"""Definition of settings to behavoirs."""
from pathlib import Path
from typing import Dict, Literal

from pydantic import BaseSettings, Field


class ArchiveSettings(BaseSettings):
    """Settings to "Archive" behavoir for accounts."""

    proc: Literal["delete", "move"]
    """Command type for IMAP4 to action."""
    options: Dict[str, str] = Field(default_factory=dict)
    """Command args."""


class AccountSettings(BaseSettings):
    """Settings for polling IMAP-server to fetch email messages."""

    host: str
    port: int
    username: str
    password: str
    inbox: str = "INBOX"
    archive: ArchiveSettings


class ApplicationSettings(BaseSettings):
    """All application settings.

    This class must be loaded from ``settings.json`` in workspace.
    """

    accounts: Dict[str, AccountSettings] = Field(default_factory=dict)


def create_new_settings(save_to: Path) -> ApplicationSettings:
    """Generate and save new settings file.

    Settings has default values.
    """
    settings = ApplicationSettings()
    save_to.write_text(settings.json())
