"""Retry policy: configures back-off strategies for step retries."""

from __future__ import annotations

import asyncio
from dataclasses import dataclass

from erp_test_agent.utils.logging import logger


@dataclass
class RetryPolicy:
    max_attempts: int = 3
    delay_seconds: float = 2.0
    backoff_factor: float = 2.0

    async def wait(self, attempt: int) -> None:
        """Sleep for the correct back-off duration before the next attempt."""
        delay = self.delay_seconds * (self.backoff_factor ** (attempt - 1))
        logger.debug(f"[RetryPolicy] Waiting {delay:.1f}s before attempt {attempt + 1}")
        await asyncio.sleep(delay)
