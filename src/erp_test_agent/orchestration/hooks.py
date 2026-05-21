"""Lifecycle hooks called at key points in the orchestration pipeline."""

from __future__ import annotations

from typing import Any, Callable, Coroutine

from erp_test_agent.domain.models import RunResult, StepResult
from erp_test_agent.utils.logging import logger

HookFn = Callable[..., Coroutine[Any, Any, None]]


class HookRegistry:
    """Allows registering async callback hooks for run lifecycle events."""

    def __init__(self) -> None:
        self._hooks: dict[str, list[HookFn]] = {}

    def on(self, event: str) -> Callable[[HookFn], HookFn]:
        """Decorator to register a hook for *event*."""
        def decorator(fn: HookFn) -> HookFn:
            self._hooks.setdefault(event, []).append(fn)
            return fn
        return decorator

    async def emit(self, event: str, **kwargs: Any) -> None:
        for fn in self._hooks.get(event, []):
            try:
                await fn(**kwargs)
            except Exception as exc:  # noqa: BLE001
                logger.error(f"[hooks] Error in hook '{event}': {exc}")


# Module-level default registry
hooks = HookRegistry()
