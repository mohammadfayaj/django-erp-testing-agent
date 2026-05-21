"""Login / logout actions."""

from __future__ import annotations

from typing import Any

from erp_test_agent.actions.base import BaseAction
from erp_test_agent.utils.logging import logger


class LoginAction(BaseAction):
    """Log in to the ERP using credentials stored in the run context."""

    name = "login"

    async def run(self, page: Any, context: dict[str, Any]) -> dict[str, Any]:
        base_url: str = context.get("base_url", "")
        username: str = context.get("username", "")
        password: str = context.get("password", "")

        logger.info(f"[login] Navigating to login page: {base_url}")
        await page.goto(f"{base_url}/accounts/login/")
        await page.wait_for_load_state("networkidle")

        await page.locator('[data-testid="input-username"]').fill(username)
        await page.locator('[data-testid="input-password"]').fill(password)
        await page.locator('[data-testid="btn-login"]').click()
        await page.wait_for_load_state("networkidle")

        logger.info(f"[login] Logged in as {username}")
        return {"logged_in": True, "username": username}


class LogoutAction(BaseAction):
    """Log out of the ERP."""

    name = "logout"

    async def run(self, page: Any, context: dict[str, Any]) -> dict[str, Any]:
        logger.info("[logout] Logging out")
        await page.locator('[data-testid="btn-logout"]').click()
        await page.wait_for_load_state("networkidle")
        return {"logged_in": False}
