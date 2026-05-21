"""Run manager: coordinates a single test plan execution end-to-end."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any

from erp_test_agent.domain.enums import RunStatus
from erp_test_agent.domain.models import RunResult, TestPlan
from erp_test_agent.executor.action_dispatcher import ActionDispatcher
from erp_test_agent.executor.browser_session import BrowserSession
from erp_test_agent.executor.playwright_runner import PlaywrightRunner
from erp_test_agent.memory.artifact_store import ArtifactStore
from erp_test_agent.memory.run_store import RunStore
from erp_test_agent.reporting.report_builder import ReportBuilder
from erp_test_agent.utils.ids import generate_run_id
from erp_test_agent.utils.logging import logger


class RunManager:
    """High-level coordinator for a single test plan run.

    Usage::

        manager = RunManager(artifact_dir=Path("./artifacts"))
        result = await manager.execute(plan, role_context={"username": ..., "password": ...})
    """

    def __init__(
        self,
        artifact_dir: Path | str = "./artifacts",
        headless: bool = True,
        slow_mo: int = 0,
        browser_type: str = "chromium",
    ) -> None:
        self._artifact_store = ArtifactStore(artifact_dir)
        self._headless = headless
        self._slow_mo = slow_mo
        self._browser_type = browser_type
        self._report_builder = ReportBuilder(
            reports_dir=self._artifact_store.reports_dir,
            runs_dir=self._artifact_store.runs_dir,
        )

    async def execute(
        self,
        plan: TestPlan,
        role_context: dict[str, Any] | None = None,
        run_id: str | None = None,
    ) -> RunResult:
        """Run *plan* and return the populated RunResult."""
        run_id = run_id or generate_run_id()
        run_dir = self._artifact_store.run_dir(run_id)

        context: dict[str, Any] = {
            "run_id": run_id,
            "artifact_dir": str(self._artifact_store.screenshots_dir),
            **(role_context or {}),
        }

        run_result = RunResult(
            run_id=run_id,
            plan=plan,
            status=RunStatus.RUNNING,
            started_at=datetime.utcnow(),
            context=context,
            artifact_dir=run_dir,
        )

        session = BrowserSession(
            browser_type=self._browser_type,
            headless=self._headless,
            slow_mo=self._slow_mo,
        )
        dispatcher = ActionDispatcher()
        runner = PlaywrightRunner(
            dispatcher=dispatcher,
            session=session,
            artifact_store=self._artifact_store,
        )

        try:
            run_result = await runner.run(plan, run_result)
        except Exception as exc:  # noqa: BLE001
            run_result.status = RunStatus.ERROR
            run_result.finished_at = datetime.utcnow()
            logger.error(f"[RunManager] Unexpected error in run {run_id}: {exc}")

        # Build reports
        try:
            self._report_builder.build(run_result)
        except Exception as exc:  # noqa: BLE001
            logger.error(f"[RunManager] Report generation failed: {exc}")

        return run_result
