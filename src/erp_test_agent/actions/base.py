"""Base action interface."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class BaseAction(ABC):
    """All actions must implement this interface.

    ``run`` receives:

    * ``page`` – the Playwright ``Page`` object
    * ``context`` – shared run context dict (read/write; steps can store IDs here)

    Returns a result dict that is merged back into the context.
    """

    #: Human-readable name used for logging / registry lookup
    name: str = ""

    @abstractmethod
    async def run(self, page: Any, context: dict[str, Any]) -> dict[str, Any]:
        """Execute the action and return a result dict."""

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}>"
