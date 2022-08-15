# noqa: D104
from dataclasses import dataclass

from ..settings import ApplicationSettings
from ..workspace import Workspace


@dataclass
class BaseSource:
    """Input for usecases."""

    settings: ApplicationSettings
    workspace: Workspace
