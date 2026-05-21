"""Workflow engine: sequences multiple test plans with dependency resolution."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from erp_test_agent.domain.enums import RunStatus
from erp_test_agent.domain.models import RunResult, TestPlan
from erp_test_agent.orchestration.run_manager import RunManager
from erp_test_agent.planner.planner import Planner
from erp_test_agent.utils.ids import generate_run_id
from erp_test_agent.utils.logging import logger


class WorkflowEngine:
    """Orchestrates multi-plan workflow execution with dependency ordering.

    Usage::

        engine = WorkflowEngine(artifact_dir="./artifacts")
        results = await engine.run_workflow(["plans/procurement/create_vendor.yaml"])
    """

    def __init__(
        self,
        artifact_dir: Path | str = "./artifacts",
        headless: bool = True,
        slow_mo: int = 0,
        browser_type: str = "chromium",
    ) -> None:
        self._planner = Planner()
        self._run_manager = RunManager(
            artifact_dir=artifact_dir,
            headless=headless,
            slow_mo=slow_mo,
            browser_type=browser_type,
        )

    async def run_workflow(
        self,
        plan_paths: list[str | Path],
        role_context: dict[str, Any] | None = None,
        run_id: str | None = None,
    ) -> list[RunResult]:
        """Load, order, compile and execute all plans in dependency order."""
        run_id = run_id or generate_run_id()

        plans = self._planner.load_plans(plan_paths)
        ordered = self._planner.resolve_order(plans)
        compiled = self._planner.compile(ordered, run_id=run_id)

        results: list[RunResult] = []
        for plan in compiled:
            logger.info(f"[WorkflowEngine] Executing plan: {plan.name}")
            result = await self._run_manager.execute(
                plan,
                role_context=role_context,
                run_id=f"{run_id}_{plan.name}",
            )
            results.append(result)
            if result.status == RunStatus.FAILED:
                logger.warning(
                    f"[WorkflowEngine] Plan '{plan.name}' FAILED – "
                    f"dependants may be skipped."
                )
        return results
