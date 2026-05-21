"""Tests for the ActionDispatcher."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from erp_test_agent.actions.base import BaseAction
from erp_test_agent.executor.action_dispatcher import ActionDispatcher


# ── Helper stubs ──────────────────────────────────────────────────────────────

class _EchoAction(BaseAction):
    name = "echo"

    async def run(self, page, context):  # type: ignore[override]
        return {"echo": context.get("data", {}).get("msg", "ok")}


class _FailAction(BaseAction):
    name = "always_fail"

    async def run(self, page, context):  # type: ignore[override]
        raise RuntimeError("intentional failure")


# ── Tests ─────────────────────────────────────────────────────────────────────

class TestActionDispatcher:
    def test_register_and_list(self) -> None:
        dispatcher = ActionDispatcher()
        dispatcher.register(_EchoAction)
        assert "echo" in dispatcher.registered_names

    def test_unknown_action_raises(self) -> None:
        dispatcher = ActionDispatcher()
        with pytest.raises(ValueError, match="Unknown action"):
            import asyncio
            asyncio.run(dispatcher.dispatch("not_a_real_action", page=None, context={}))

    @pytest.mark.asyncio
    async def test_builtin_actions_registered(self) -> None:
        dispatcher = ActionDispatcher()
        expected = [
            "login",
            "logout",
            "navigate",
            "submit_form",
            "create_vendor",
            "create_customer",
            "create_employee",
            "verify_record",
            "capture_screenshot",
        ]
        for name in expected:
            assert name in dispatcher.registered_names, f"Missing built-in: {name}"

    @pytest.mark.asyncio
    async def test_dispatch_echo_action(self) -> None:
        dispatcher = ActionDispatcher(extra_actions=[_EchoAction])
        result = await dispatcher.dispatch(
            "echo",
            page=None,
            context={"data": {"msg": "hello"}},
        )
        assert result == {"echo": "hello"}

    @pytest.mark.asyncio
    async def test_dispatch_propagates_exception(self) -> None:
        dispatcher = ActionDispatcher(extra_actions=[_FailAction])
        with pytest.raises(RuntimeError, match="intentional failure"):
            await dispatcher.dispatch("always_fail", page=None, context={})

    def test_custom_action_overrides_builtin_if_same_name(self) -> None:
        class _CustomLogin(BaseAction):
            name = "login"
            async def run(self, page, context):
                return {"custom": True}

        dispatcher = ActionDispatcher(extra_actions=[_CustomLogin])
        # Custom registered last should override
        assert dispatcher._registry["login"] is _CustomLogin
