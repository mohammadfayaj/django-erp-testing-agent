"""Generic form-level actions."""

from __future__ import annotations

from typing import Any

from erp_test_agent.actions.base import BaseAction
from erp_test_agent.utils.logging import logger


class SubmitFormAction(BaseAction):
    """Click the primary save/submit button on the current form."""

    name = "submit_form"

    async def run(self, page: Any, context: dict[str, Any]) -> dict[str, Any]:
        logger.info("[submit_form] Submitting form")
        await page.locator('[data-testid="btn-save"]').click()
        await page.wait_for_load_state("networkidle")
        return {"form_submitted": True}


class FillFieldAction(BaseAction):
    """Fill a single named form field."""

    name = "fill_field"

    async def run(self, page: Any, context: dict[str, Any]) -> dict[str, Any]:
        data = context.get("data", {})
        selector: str = data["selector"]
        value: str = str(data["value"])
        logger.debug(f"[fill_field] {selector} = {value!r}")
        await page.locator(selector).fill(value)
        return {"filled": selector}


class SelectOptionAction(BaseAction):
    """Select a dropdown option by label."""

    name = "select_option"

    async def run(self, page: Any, context: dict[str, Any]) -> dict[str, Any]:
        data = context.get("data", {})
        selector: str = data["selector"]
        label: str = data["label"]
        logger.debug(f"[select_option] {selector} → {label!r}")
        await page.locator(selector).select_option(label=label)
        return {"selected": label}


class CreateVendorAction(BaseAction):
    """Create a new vendor using standard procurement form fields."""

    name = "create_vendor"

    async def run(self, page: Any, context: dict[str, Any]) -> dict[str, Any]:
        data = context.get("data", {})
        logger.info(f"[create_vendor] Creating vendor: {data.get('vendor_name')}")

        await page.locator('[data-testid="btn-new-vendor"]').click()
        await page.locator('[data-testid="vendor-name"]').fill(data["vendor_name"])

        if vat := data.get("vat_number"):
            await page.locator('[data-testid="vendor-vat"]').fill(vat)
        if country := data.get("country"):
            await page.locator('[data-testid="vendor-country"]').select_option(label=country)
        if city := data.get("city"):
            await page.locator('[data-testid="vendor-city"]').fill(city)
        if terms := data.get("payment_terms"):
            await page.locator('[data-testid="vendor-payment-terms"]').select_option(label=terms)

        await page.locator('[data-testid="btn-save"]').click()
        await page.wait_for_load_state("networkidle")
        return {"vendor_name": data["vendor_name"]}


class CreateCustomerAction(BaseAction):
    """Create a new customer using standard sales form fields."""

    name = "create_customer"

    async def run(self, page: Any, context: dict[str, Any]) -> dict[str, Any]:
        data = context.get("data", {})
        logger.info(f"[create_customer] Creating customer: {data.get('customer_name')}")

        await page.locator('[data-testid="btn-new-customer"]').click()
        await page.locator('[data-testid="customer-name"]').fill(data["customer_name"])

        if vat := data.get("vat_number"):
            await page.locator('[data-testid="customer-vat"]').fill(vat)
        if country := data.get("country"):
            await page.locator('[data-testid="customer-country"]').select_option(label=country)
        if city := data.get("city"):
            await page.locator('[data-testid="customer-city"]').fill(city)
        if limit := data.get("credit_limit"):
            await page.locator('[data-testid="customer-credit-limit"]').fill(str(limit))

        await page.locator('[data-testid="btn-save"]').click()
        await page.wait_for_load_state("networkidle")
        return {"customer_name": data["customer_name"]}


class CreateEmployeeAction(BaseAction):
    """Create a new employee in the HR module."""

    name = "create_employee"

    async def run(self, page: Any, context: dict[str, Any]) -> dict[str, Any]:
        data = context.get("data", {})
        full_name = f"{data.get('first_name', '')} {data.get('last_name', '')}".strip()
        logger.info(f"[create_employee] Creating employee: {full_name}")

        await page.locator('[data-testid="btn-new-employee"]').click()
        await page.locator('[data-testid="employee-first-name"]').fill(data.get("first_name", ""))
        await page.locator('[data-testid="employee-last-name"]').fill(data.get("last_name", ""))

        if nid := data.get("national_id"):
            await page.locator('[data-testid="employee-national-id"]').fill(nid)
        if dept := data.get("department"):
            await page.locator('[data-testid="employee-department"]').select_option(label=dept)
        if title := data.get("job_title"):
            await page.locator('[data-testid="employee-job-title"]').fill(title)
        if hire := data.get("hire_date"):
            await page.locator('[data-testid="employee-hire-date"]').fill(hire)

        await page.locator('[data-testid="btn-save"]').click()
        await page.wait_for_load_state("networkidle")
        return {"employee_name": full_name}


class VerifyRecordAction(BaseAction):
    """Assert that the current page shows the expected record status."""

    name = "verify_record"

    async def run(self, page: Any, context: dict[str, Any]) -> dict[str, Any]:
        data = context.get("data", {})
        expected_status = data.get("expected_status")
        target = data.get("target", "record")

        if expected_status:
            status_text = await page.locator('[data-testid="record-status"]').inner_text()
            assert status_text.strip() == expected_status, (
                f"[verify_record] {target} status mismatch: "
                f"expected={expected_status!r} actual={status_text!r}"
            )
        logger.info(f"[verify_record] {target} verified (status={expected_status})")
        return {"verified": True, "target": target}


class CaptureScreenshotAction(BaseAction):
    """Take a screenshot and save it to the artifact store."""

    name = "capture_screenshot"

    async def run(self, page: Any, context: dict[str, Any]) -> dict[str, Any]:
        import os
        from pathlib import Path

        data = context.get("data", {})
        artifact_dir = Path(context.get("artifact_dir", "./artifacts/screenshots"))
        artifact_dir.mkdir(parents=True, exist_ok=True)

        filename = data.get("filename", f"screenshot_{context.get('run_id', 'run')}.png")
        path = artifact_dir / filename
        await page.screenshot(path=str(path))
        logger.info(f"[capture_screenshot] Saved: {path}")
        return {"screenshot": str(path)}
