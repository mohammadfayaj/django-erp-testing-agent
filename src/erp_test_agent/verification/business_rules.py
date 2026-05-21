"""Business rule validators for financial and ERP-specific logic."""

from __future__ import annotations

from decimal import Decimal
from typing import Any

from erp_test_agent.utils.logging import logger


def validate_debit_equals_credit(lines: list[dict[str, Any]]) -> bool:
    """Validate that total debits equal total credits in a journal entry."""
    total_debit = sum(Decimal(str(line.get("debit", 0))) for line in lines)
    total_credit = sum(Decimal(str(line.get("credit", 0))) for line in lines)
    balanced = total_debit == total_credit
    if not balanced:
        logger.error(
            f"[business_rule] Debit/Credit mismatch: debit={total_debit} credit={total_credit}"
        )
    return balanced


def validate_vat_amount(subtotal: Decimal, vat_rate: Decimal, vat_amount: Decimal) -> bool:
    """Validate that the VAT amount matches the expected formula."""
    expected = (subtotal * vat_rate / Decimal("100")).quantize(Decimal("0.01"))
    actual = vat_amount.quantize(Decimal("0.01"))
    match = expected == actual
    if not match:
        logger.error(
            f"[business_rule] VAT mismatch: expected={expected} actual={actual}"
        )
    return match


def validate_net_salary(
    basic: Decimal,
    allowances: Decimal,
    deductions: Decimal,
    net: Decimal,
) -> bool:
    """Validate net salary = basic + allowances - deductions."""
    expected = (basic + allowances - deductions).quantize(Decimal("0.01"))
    actual = net.quantize(Decimal("0.01"))
    match = expected == actual
    if not match:
        logger.error(
            f"[business_rule] Net salary mismatch: expected={expected} actual={actual}"
        )
    return match


def validate_balance_sheet(
    total_assets: Decimal,
    total_liabilities: Decimal,
    total_equity: Decimal,
) -> bool:
    """Assets = Liabilities + Equity."""
    expected = (total_liabilities + total_equity).quantize(Decimal("0.01"))
    actual = total_assets.quantize(Decimal("0.01"))
    balanced = expected == actual
    if not balanced:
        logger.error(
            f"[business_rule] Balance sheet unbalanced: "
            f"assets={actual} liabilities+equity={expected}"
        )
    return balanced
