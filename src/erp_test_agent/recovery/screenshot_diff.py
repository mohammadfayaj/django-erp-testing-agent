"""Screenshot diff: detect unexpected page state changes."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from erp_test_agent.utils.logging import logger


async def capture_for_diff(page: Any, path: Path) -> None:
    """Capture a screenshot for visual diffing."""
    path.parent.mkdir(parents=True, exist_ok=True)
    await page.screenshot(path=str(path), full_page=True)
    logger.debug(f"[screenshot_diff] Captured: {path}")
