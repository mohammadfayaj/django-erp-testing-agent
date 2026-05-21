"""Run store: persists and retrieves run results from the filesystem."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from erp_test_agent.domain.enums import RunStatus, StepStatus
from erp_test_agent.domain.models import RunResult
from erp_test_agent.utils.logging import logger


class RunStore:
    """Serialises/deserialises RunResult summaries to JSON files."""

    def __init__(self, runs_dir: Path | str) -> None:
        self.runs_dir = Path(runs_dir)
        self.runs_dir.mkdir(parents=True, exist_ok=True)

    def save(self, run_result: RunResult) -> Path:
        """Persist a run summary to <runs_dir>/<run_id>/result.json."""
        run_dir = self.runs_dir / run_result.run_id
        run_dir.mkdir(parents=True, exist_ok=True)
        path = run_dir / "result.json"
        data = self._serialize(run_result)
        path.write_text(json.dumps(data, indent=2, default=str))
        logger.info(f"[RunStore] Saved run result: {path}")
        return path

    def load(self, run_id: str) -> dict[str, Any]:
        """Load a previously saved run summary."""
        path = self.runs_dir / run_id / "result.json"
        if not path.exists():
            raise FileNotFoundError(f"Run not found: {run_id}")
        return json.loads(path.read_text())

    @staticmethod
    def _serialize(run_result: RunResult) -> dict[str, Any]:
        return {
            "run_id": run_result.run_id,
            "plan": run_result.plan.name,
            "department": run_result.plan.department,
            "status": run_result.status.value,
            "started_at": run_result.started_at.isoformat(),
            "finished_at": (
                run_result.finished_at.isoformat() if run_result.finished_at else None
            ),
            "duration_ms": run_result.duration_ms,
            "passed": run_result.passed,
            "failed": run_result.failed,
            "steps": [
                {
                    "action": r.step.action,
                    "status": r.status.value,
                    "attempt": r.attempt,
                    "duration_ms": r.duration_ms,
                    "error": r.error,
                    "screenshot": str(r.screenshot) if r.screenshot else None,
                }
                for r in run_result.step_results
            ],
        }
