"""JUnit XML report generator."""

from __future__ import annotations

import xml.etree.ElementTree as ET
from pathlib import Path

from erp_test_agent.domain.enums import StepStatus
from erp_test_agent.domain.models import RunResult
from erp_test_agent.utils.logging import logger


def render_junit_report(result: RunResult, output_path: Path) -> Path:
    """Write a JUnit-compatible XML report to *output_path*."""
    suite = ET.Element(
        "testsuite",
        name=result.plan.name,
        tests=str(len(result.step_results)),
        failures=str(result.failed),
        errors="0",
        time=f"{result.duration_ms / 1000:.3f}",
    )
    for sr in result.step_results:
        case = ET.SubElement(
            suite,
            "testcase",
            name=sr.step.action,
            classname=result.plan.department,
            time=f"{sr.duration_ms / 1000:.3f}",
        )
        if sr.status == StepStatus.FAILED:
            failure = ET.SubElement(case, "failure", message=sr.error or "")
            failure.text = sr.error or ""

    tree = ET.ElementTree(suite)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    tree.write(str(output_path), encoding="unicode", xml_declaration=True)
    logger.info(f"[junit] Written: {output_path}")
    return output_path
