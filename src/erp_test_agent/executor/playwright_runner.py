"""Playwright runner: executes a compiled test plan step by step."""

from __future__ import annotations

import asyncio
from datetime import datetime
from pathlib import Path
from typing import Any

from erp_test_agent.domain.enums import RunStatus, StepStatus
from erp_test_agent.domain.models import RunResult, StepResult, TestPlan
from erp_test_agent.executor.action_dispatcher import ActionDispatcher
from erp_test_agent.executor.browser_session import BrowserSession
from erp_test_agent.memory.artifact_store import ArtifactStore
from erp_test_agent.utils.logging import logger


class PlaywrightRunner:
    """Executes all steps in a test plan using a Playwright browser session.

    Each step's data dict is merged with the shared run context before dispatch.
    Results from each step are merged back into the context so later steps can
    reference IDs / names created in earlier steps.
    """

    def __init__(
        self,
        dispatcher: ActionDispatcher | None = None,
        session: BrowserSession | None = None,
        artifact_store: ArtifactStore | None = None,
    ) -> None:
        self._dispatcher = dispatcher or ActionDispatcher()
        self._session = session
        self._artifact_store = artifact_store

    async def run(
        self,
        plan: TestPlan,
        run_result: RunResult,
    ) -> RunResult:
        """Execute the plan and populate *run_result* with step outcomes."""
        base_context: dict[str, Any] = dict(run_result.context)
        base_context["run_id"] = run_result.run_id
        if self._artifact_store:
            base_context["artifact_dir"] = str(self._artifact_store.screenshots_dir)

        async with (self._session or BrowserSession()) as session:
            page = await session.new_page()
            run_result.status = RunStatus.RUNNING

            for idx, step in enumerate(plan.steps):
                step_context = {**base_context, "data": step.data}
                started = datetime.utcnow()
                attempt = 0

                for attempt in range(1, step.retry + 1):
                    try:
                        output = await self._dispatcher.dispatch(
                            step.action, page, step_context
                        )
                        # Merge output back into shared context
                        base_context.update(output)
                        run_result.context.update(output)

                        elapsed = (datetime.utcnow() - started).total_seconds() * 1000
                        result = StepResult(
                            step=step,
                            status=StepStatus.PASSED,
                            output=output,
                            duration_ms=elapsed,
                            attempt=attempt,
                        )
                        step.status = StepStatus.PASSED
                        logger.info(
                            f"[Runner] ✓ Step {idx + 1}/{len(plan.steps)}: {step.action}"
                        )
                        break

                    except Exception as exc:  # noqa: BLE001
                        if attempt < step.retry:
                            logger.warning(
                                f"[Runner] Step {step.action} failed (attempt {attempt}), retrying: {exc}"
                            )
                            await asyncio.sleep(2)
                            continue

                        elapsed = (datetime.utcnow() - started).total_seconds() * 1000
                        screenshot_path: Path | None = None
                        if self._artifact_store:
                            screenshot_path = self._artifact_store.screenshots_dir / (
                                f"fail_{run_result.run_id}_step{idx:03d}.png"
                            )
                            try:
                                await page.screenshot(path=str(screenshot_path))
                            except Exception:  # noqa: BLE001
                                screenshot_path = None

                        result = StepResult(
                            step=step,
                            status=StepStatus.FAILED,
                            error=str(exc),
                            screenshot=screenshot_path,
                            duration_ms=elapsed,
                            attempt=attempt,
                        )
                        step.status = StepStatus.FAILED
                        logger.error(
                            f"[Runner] ✗ Step {idx + 1}/{len(plan.steps)}: {step.action} → {exc}"
                        )

                run_result.step_results.append(result)

            run_result.status = (
                RunStatus.PASSED if run_result.failed == 0 else RunStatus.FAILED
            )
            run_result.finished_at = datetime.utcnow()

            # Save trace
            if self._artifact_store:
                trace_path = str(
                    self._artifact_store.traces_dir / f"{run_result.run_id}.zip"
                )
                try:
                    await session.save_trace(trace_path)
                except Exception:  # noqa: BLE001
                    pass

        return run_result
