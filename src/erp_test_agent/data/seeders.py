"""Test data seeders: helper functions to pre-populate required master data."""

from __future__ import annotations

from typing import Any


async def ensure_vendor_exists(page: Any, context: dict[str, Any]) -> bool:
    """Return True if the vendor already exists, False if it needs to be created."""
    vendor_name = context.get("vendor_name", "")
    content = await page.content()
    return vendor_name in content


async def ensure_customer_exists(page: Any, context: dict[str, Any]) -> bool:
    """Return True if the customer already exists."""
    customer_name = context.get("customer_name", "")
    content = await page.content()
    return customer_name in content
