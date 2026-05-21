"""Assertion actions: verify UI state during a test run."""

from __future__ import annotations

from typing import Any

from erp_test_agent.actions.base import BaseAction
from erp_test_agent.utils.logging import logger


class AssertUIContainsAction(BaseAction):
    """Assert that the current page contains a text string."""

    name = "assert_ui_contains"

    async def run(self, page: Any, context: dict[str, Any]) -> dict[str, Any]:
        data = context.get("data", {})
        text: str = data["text"]
        logger.debug(f"[assert_ui_contains] Checking for text: {text!r}")
        content = await page.content()
        assert text in content, f"Expected text {text!r} not found in page"
        return {"assertion": "ui_contains", "text": text, "passed": True}


class AssertFieldEqualsAction(BaseAction):
    """Assert that a labelled field equals an expected value."""

    name = "assert_field_equals"

    async def run(self, page: Any, context: dict[str, Any]) -> dict[str, Any]:
        data = context.get("data", {})
        field: str = data["field"]
        expected: str = str(data["expected"])

        selector = f'[data-testid="field-{field}"]'
        actual = await page.locator(selector).inner_text()
        assert actual.strip() == expected, (
            f"[assert_field_equals] field={field!r} expected={expected!r} actual={actual!r}"
        )
        logger.debug(f"[assert_field_equals] {field} = {expected!r} ✓")
        return {"assertion": "field_equals", "field": field, "passed": True}
