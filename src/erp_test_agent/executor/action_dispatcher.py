"""Action dispatcher: maps action name strings to action classes."""

from __future__ import annotations

from typing import Any, Type

from erp_test_agent.actions.assertion_actions import (
    AssertFieldEqualsAction,
    AssertUIContainsAction,
)
from erp_test_agent.actions.base import BaseAction
from erp_test_agent.actions.form_actions import (
    CaptureScreenshotAction,
    CreateCustomerAction,
    CreateEmployeeAction,
    CreateVendorAction,
    FillFieldAction,
    SelectOptionAction,
    SubmitFormAction,
    VerifyRecordAction,
)
from erp_test_agent.actions.login import LoginAction, LogoutAction
from erp_test_agent.actions.navigation import NavigateAction
from erp_test_agent.actions.table_actions import ClickRowAction, SearchTableAction
from erp_test_agent.actions.upload_actions import UploadFileAction
from erp_test_agent.utils.logging import logger

_BUILTIN_ACTIONS: list[Type[BaseAction]] = [
    LoginAction,
    LogoutAction,
    NavigateAction,
    SubmitFormAction,
    FillFieldAction,
    SelectOptionAction,
    CreateVendorAction,
    CreateCustomerAction,
    CreateEmployeeAction,
    VerifyRecordAction,
    CaptureScreenshotAction,
    SearchTableAction,
    ClickRowAction,
    UploadFileAction,
    AssertUIContainsAction,
    AssertFieldEqualsAction,
]


class ActionDispatcher:
    """Resolves an action name to its implementation and executes it.

    Usage::

        dispatcher = ActionDispatcher()
        result = await dispatcher.dispatch("login", page, context)
    """

    def __init__(self, extra_actions: list[Type[BaseAction]] | None = None) -> None:
        self._registry: dict[str, Type[BaseAction]] = {}
        for cls in _BUILTIN_ACTIONS:
            self.register(cls)
        for cls in (extra_actions or []):
            self.register(cls)

    def register(self, action_cls: Type[BaseAction]) -> None:
        """Register a custom action class."""
        key = action_cls.name
        if not key:
            raise ValueError(f"{action_cls} has no 'name' attribute set")
        self._registry[key] = action_cls
        logger.debug(f"[ActionDispatcher] Registered action: {key}")

    async def dispatch(
        self,
        action_name: str,
        page: Any,
        context: dict[str, Any],
    ) -> dict[str, Any]:
        """Look up and run the action; return its result dict."""
        action_cls = self._registry.get(action_name)
        if action_cls is None:
            raise ValueError(
                f"Unknown action: '{action_name}'. "
                f"Registered actions: {sorted(self._registry)}"
            )
        action = action_cls()
        logger.info(f"[ActionDispatcher] Running: {action_name}")
        return await action.run(page, context)

    @property
    def registered_names(self) -> list[str]:
        return sorted(self._registry)
