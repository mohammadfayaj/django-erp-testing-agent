"""Navigation actions: move between ERP modules."""

from __future__ import annotations

from typing import Any

from erp_test_agent.actions.base import BaseAction
from erp_test_agent.utils.logging import logger


class NavigateAction(BaseAction):
    """Navigate to a module (and optionally sub-module) in the ERP."""

    name = "navigate"

    async def run(self, page: Any, context: dict[str, Any]) -> dict[str, Any]:
        data: dict[str, Any] = context.get("data", {})
        base_url: str = context.get("base_url", "")
        modules_cfg: dict = context.get("modules_cfg", {})

        module = data.get("module", "")
        sub_module = data.get("sub_module")

        module_cfg = modules_cfg.get(module, {})
        if sub_module:
            path = module_cfg.get("sub_modules", {}).get(sub_module, f"/{module}/{sub_module}/")
        else:
            path = module_cfg.get("url_path", f"/{module}/")

        url = f"{base_url}{path}"
        logger.info(f"[navigate] → {url}")
        await page.goto(url)
        await page.wait_for_load_state("networkidle")
        return {"current_module": module, "current_url": url}
