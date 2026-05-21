"""Test data factories: generate idempotency-safe test data names."""

from __future__ import annotations

from datetime import date


def vendor_name(run_id: str) -> str:
    return f"vendor_auto_{run_id}"


def customer_name(run_id: str) -> str:
    return f"customer_auto_{run_id}"


def employee_name(run_id: str) -> str:
    return f"employee_auto_{run_id}"


def journal_reference(run_id: str) -> str:
    return f"JE-AUTO-{run_id}"


def po_reference(run_id: str) -> str:
    return f"PO-AUTO-{run_id}"


def so_reference(run_id: str) -> str:
    return f"SO-AUTO-{run_id}"


def payroll_period(year: int | None = None, month: int | None = None) -> str:
    today = date.today()
    y = year or today.year
    m = month or today.month
    return f"{y:04d}-{m:02d}"
