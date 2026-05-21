"""Recovery: fallback locator strategies when primary locators fail."""

from __future__ import annotations

from typing import Any

from erp_test_agent.utils.logging import logger

#: Priority-ordered fallback strategies per element type
FALLBACK_MAP: dict[str, list[str]] = {
    "btn-save": [
        '[data-testid="btn-save"]',
        'button[type="submit"]',
        'button:has-text("Save")',
        'button:has-text("حفظ")',
    ],
    "btn-new": [
        '[data-testid^="btn-new"]',
        'a:has-text("New")',
        'button:has-text("Add")',
    ],
    "record-status": [
        '[data-testid="record-status"]',
        '.status-badge',
        '.record-status',
        'span:has-text("Status")',
    ],
}


async def try_fallback_locator(
    page: Any,
    element_key: str,
    action: str = "click",
) -> bool:
    """Try each fallback locator in order; return True on first success."""
    candidates = FALLBACK_MAP.get(element_key, [])
    for selector in candidates:
        try:
            locator = page.locator(selector).first
            if await locator.count() > 0:
                if action == "click":
                    await locator.click()
                logger.info(
                    f"[fallback_locators] Succeeded with fallback: {selector}"
                )
                return True
        except Exception:  # noqa: BLE001
            continue
    logger.error(f"[fallback_locators] All fallbacks exhausted for: {element_key}")
    return False
