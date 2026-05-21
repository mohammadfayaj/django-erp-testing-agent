"""File upload actions."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from erp_test_agent.actions.base import BaseAction
from erp_test_agent.utils.logging import logger


class UploadFileAction(BaseAction):
    """Upload a file via a file-input element."""

    name = "upload_file"

    async def run(self, page: Any, context: dict[str, Any]) -> dict[str, Any]:
        data = context.get("data", {})
        selector: str = data.get("selector", '[data-testid="file-upload"]')
        file_path: str = data["file_path"]

        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Upload file not found: {path}")

        logger.info(f"[upload_file] Uploading {path} to {selector}")
        await page.locator(selector).set_input_files(str(path))
        return {"uploaded": str(path)}
