"""API checks: verify business results via HTTP endpoints."""

from __future__ import annotations

from typing import Any

import httpx

from erp_test_agent.utils.logging import logger


async def get_record(base_url: str, endpoint: str, token: str = "") -> dict[str, Any]:
    """Fetch a JSON record from the ERP API."""
    headers = {"Authorization": f"Token {token}"} if token else {}
    async with httpx.AsyncClient(base_url=base_url, headers=headers) as client:
        response = await client.get(endpoint)
        response.raise_for_status()
        return response.json()


async def assert_record_exists_api(
    base_url: str,
    endpoint: str,
    token: str = "",
) -> bool:
    """Return True if the API endpoint returns a 200 response."""
    try:
        await get_record(base_url, endpoint, token)
        return True
    except httpx.HTTPStatusError as exc:
        logger.warning(f"[api_check] Record not found at {endpoint}: {exc}")
        return False
