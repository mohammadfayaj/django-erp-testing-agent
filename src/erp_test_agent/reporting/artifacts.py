"""Artifact collector: gathers screenshots, traces, and reports."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from erp_test_agent.domain.models import RunResult
from erp_test_agent.utils.logging import logger


def list_screenshots(result: RunResult) -> list[Path]:
    """Return all screenshot paths from a run result."""
    paths = []
    for sr in result.step_results:
        if sr.screenshot and Path(sr.screenshot).exists():
            paths.append(Path(sr.screenshot))
    return paths


def collect_artifacts(result: RunResult, run_dir: Path) -> dict[str, Any]:
    """Copy / catalogue all artifacts for a run."""
    manifest: dict[str, Any] = {
        "run_id": result.run_id,
        "screenshots": [str(p) for p in list_screenshots(result)],
        "trace": str(run_dir / "trace.zip")
        if (run_dir / "trace.zip").exists()
        else None,
        "reports": {
            "html": str(run_dir / "report.html"),
            "json": str(run_dir / "result.json"),
            "junit": str(run_dir / "junit.xml"),
        },
    }
    logger.debug(f"[artifacts] Manifest for {result.run_id}: {manifest}")
    return manifest
