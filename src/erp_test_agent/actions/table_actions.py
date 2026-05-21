"""Table / list view actions."""

from __future__ import annotations

from typing import Any

from erp_test_agent.actions.base import BaseAction
from erp_test_agent.utils.logging import logger


class SearchTableAction(BaseAction):
    """Search for a record in a list/table view."""

    name = "search_table"

    async def run(self, page: Any, context: dict[str, Any]) -> dict[str, Any]:
        data = context.get("data", {})
        query: str = data.get("query", "")
        logger.info(f"[search_table] Searching for: {query!r}")
        search = page.locator('[data-testid="table-search"]')
        await search.fill(query)
        await search.press("Enter")
        await page.wait_for_load_state("networkidle")
        return {"searched": query}


class ClickRowAction(BaseAction):
    """Click a row in a table by index (0-based) or by matching text."""

    name = "click_row"

    async def run(self, page: Any, context: dict[str, Any]) -> dict[str, Any]:
        data = context.get("data", {})
        index: int = data.get("index", 0)
        match_text: str | None = data.get("match_text")

        if match_text:
            row = page.locator("tr", has_text=match_text).first
        else:
            row = page.locator("tbody tr").nth(index)

        await row.click()
        await page.wait_for_load_state("networkidle")
        logger.info(f"[click_row] Clicked row (index={index}, match_text={match_text!r})")
        return {"row_clicked": True}
