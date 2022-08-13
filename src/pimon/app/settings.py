"""Definition of settings to behavoirs."""
from pathlib import Path
from typing import Dict, Literal

import tomli
import tomli_w
from pydantic import BaseSettings, Field


class RemoveSettings(BaseSettings):
    """Settings for behavoir to remove from INBOX in accounts."""

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
    remove: RemoveSettings


class ApplicationSettings(BaseSettings):
    """All application settings.

    This class must be loaded from ``settings.json`` in workspace.
    """

    accounts: Dict[str, AccountSettings] = Field(default_factory=dict)

    @classmethod
    def load(cls, src_path: Path) -> "ApplicationSettings":
        """Load settings from TOML-file."""
        obj = tomli.loads(src_path.read_text())
        return cls(**obj)

    def save(self, dst: Path):
        """Save settings as TOML-file."""
        dst.write_text(tomli_w.dumps(self.dict()))


def create_new_settings(save_to: Path) -> ApplicationSettings:
    """Generate and save new settings file.

    Settings has default values.
    """
    settings = ApplicationSettings()
    settings.save(save_to)
