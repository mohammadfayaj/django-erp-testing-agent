"""Browser session management (one context per role / test run)."""

from __future__ import annotations

from typing import Any

from playwright.async_api import Browser, BrowserContext, Page, Playwright, async_playwright

from erp_test_agent.domain.enums import Browser as BrowserEnum
from erp_test_agent.utils.logging import logger


class BrowserSession:
    """Manages a Playwright browser session.

    One session should be created per test run.  It owns the browser context
    and provides isolated pages.
    """

    def __init__(
        self,
        browser_type: str = BrowserEnum.CHROMIUM,
        headless: bool = True,
        slow_mo: int = 0,
        timeout: int = 30_000,
        trace: str = "retain-on-failure",
    ) -> None:
        self._browser_type = browser_type
        self._headless = headless
        self._slow_mo = slow_mo
        self._timeout = timeout
        self._trace = trace

        self._playwright: Playwright | None = None
        self._browser: Browser | None = None
        self._context: BrowserContext | None = None

    async def start(self) -> None:
        """Launch the browser and create an isolated context."""
        self._playwright = await async_playwright().start()
        launcher = getattr(self._playwright, self._browser_type)
        self._browser = await launcher.launch(
            headless=self._headless,
            slow_mo=self._slow_mo,
        )
        self._context = await self._browser.new_context(
            viewport={"width": 1280, "height": 900},
            record_video_dir=None,
        )
        self._context.set_default_timeout(self._timeout)
        if self._trace in ("on", "retain-on-failure"):
            await self._context.tracing.start(screenshots=True, snapshots=True)
        logger.info(
            f"[BrowserSession] Started {self._browser_type} "
            f"(headless={self._headless}, slow_mo={self._slow_mo})"
        )

    async def new_page(self) -> Page:
        if self._context is None:
            raise RuntimeError("BrowserSession.start() must be called first")
        return await self._context.new_page()

    async def save_trace(self, path: str) -> None:
        if self._context and self._trace in ("on", "retain-on-failure"):
            await self._context.tracing.stop(path=path)
            logger.info(f"[BrowserSession] Trace saved: {path}")

    async def stop(self, trace_path: str | None = None) -> None:
        if trace_path:
            await self.save_trace(trace_path)
        if self._context:
            await self._context.close()
        if self._browser:
            await self._browser.close()
        if self._playwright:
            await self._playwright.stop()
        logger.info("[BrowserSession] Browser stopped")

    async def __aenter__(self) -> "BrowserSession":
        await self.start()
        return self

    async def __aexit__(self, *_: Any) -> None:
        await self.stop()
