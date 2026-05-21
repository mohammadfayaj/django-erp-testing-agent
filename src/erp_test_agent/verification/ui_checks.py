"""UI checks: verify expected elements and text on the page."""

from __future__ import annotations

from typing import Any

from erp_test_agent.utils.logging import logger


async def assert_text_present(page: Any, text: str) -> bool:
    """Return True if the given text is present anywhere on the page."""
    content = await page.content()
    present = text in content
    if not present:
        logger.warning(f"[ui_check] Text not found: {text!r}")
    return present


async def assert_field_value(page: Any, selector: str, expected: str) -> bool:
    """Return True if the element's inner text matches *expected*."""
    try:
        actual = await page.locator(selector).inner_text(timeout=5_000)
        match = actual.strip() == expected
        if not match:
            logger.warning(
                f"[ui_check] Field mismatch {selector}: "
                f"expected={expected!r} actual={actual!r}"
            )
        return match
    except Exception as exc:  # noqa: BLE001
        logger.error(f"[ui_check] Error reading {selector}: {exc}")
        return False


async def assert_record_status(page: Any, expected_status: str) -> bool:
    """Assert that the [data-testid='record-status'] element shows the expected value."""
    return await assert_field_value(page, '[data-testid="record-status"]', expected_status)
