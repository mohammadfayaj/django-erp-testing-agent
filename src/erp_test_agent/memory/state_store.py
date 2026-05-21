"""State store: persists the shared run context (checkpoints between steps)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from erp_test_agent.utils.logging import logger


class StateStore:
    """Stores checkpoint data so partial runs can be resumed.

    The state is written to <runs_dir>/<run_id>/state.json after every step.
    """

    def __init__(self, run_dir: Path | str) -> None:
        self.run_dir = Path(run_dir)
        self.run_dir.mkdir(parents=True, exist_ok=True)
        self._path = self.run_dir / "state.json"
        self._state: dict[str, Any] = {}

    def load(self) -> dict[str, Any]:
        if self._path.exists():
            self._state = json.loads(self._path.read_text())
            logger.debug(f"[StateStore] Loaded state from {self._path}")
        return self._state

    def save(self, state: dict[str, Any]) -> None:
        self._state.update(state)
        self._path.write_text(json.dumps(self._state, indent=2, default=str))
        logger.debug(f"[StateStore] State saved: {self._path}")

    def get(self, key: str, default: Any = None) -> Any:
        return self._state.get(key, default)

    def set(self, key: str, value: Any) -> None:
        self._state[key] = value
        self.save(self._state)
