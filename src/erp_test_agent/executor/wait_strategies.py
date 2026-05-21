"""Wait strategies for Playwright page interactions."""

from __future__ import annotations

from typing import Any

from erp_test_agent.utils.logging import logger


async def wait_for_navigation(page: Any, timeout: int = 30_000) -> None:
    """Wait for the page to finish loading after navigation."""
    await page.wait_for_load_state("networkidle", timeout=timeout)


async def wait_for_selector(page: Any, selector: str, timeout: int = 30_000) -> None:
    """Wait for a selector to become visible."""
    await page.wait_for_selector(selector, state="visible", timeout=timeout)


async def wait_for_text(page: Any, text: str, timeout: int = 30_000) -> None:
    """Wait for specific text to appear anywhere on the page."""
    await page.wait_for_function(
        f'document.body.innerText.includes("{text}")',
        timeout=timeout,
    )


async def wait_for_url_contains(page: Any, substring: str, timeout: int = 30_000) -> None:
    """Wait until the current URL contains a given substring."""
    await page.wait_for_url(f"**{substring}**", timeout=timeout)
