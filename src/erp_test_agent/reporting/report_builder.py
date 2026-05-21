"""Report builder: orchestrates all report formats for a run result."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from erp_test_agent.domain.models import RunResult
from erp_test_agent.memory.run_store import RunStore
from erp_test_agent.reporting.artifacts import collect_artifacts
from erp_test_agent.reporting.html_report import render_html_report
from erp_test_agent.reporting.junit import render_junit_report
from erp_test_agent.utils.logging import logger


class ReportBuilder:
    """Generates all configured report formats and stores them under *reports_dir*."""

    def __init__(
        self,
        reports_dir: Path | str = "./artifacts/reports",
        runs_dir: Path | str = "./artifacts/runs",
    ) -> None:
        self.reports_dir = Path(reports_dir)
        self._run_store = RunStore(runs_dir)

    def build(self, result: RunResult) -> dict[str, Any]:
        """Generate all reports and return a manifest dict."""
        run_dir = self.reports_dir / result.run_id
        run_dir.mkdir(parents=True, exist_ok=True)

        # JSON (via RunStore)
        json_path = self._run_store.save(result)

        # HTML
        html_path = run_dir / "report.html"
        render_html_report(result, html_path)

        # JUnit XML
        junit_path = run_dir / "junit.xml"
        render_junit_report(result, junit_path)

        manifest = collect_artifacts(result, run_dir)
        logger.info(
            f"[ReportBuilder] Reports for {result.run_id}: "
            f"html={html_path} junit={junit_path}"
        )
        return manifest
