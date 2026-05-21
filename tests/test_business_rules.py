"""Tests for business rule validators."""

from __future__ import annotations

from decimal import Decimal

import pytest

from erp_test_agent.verification.business_rules import (
    validate_balance_sheet,
    validate_debit_equals_credit,
    validate_net_salary,
    validate_vat_amount,
)


class TestDebitEqualsCredit:
    def test_balanced_entry(self) -> None:
        lines = [
            {"debit": "5000", "credit": "0"},
            {"debit": "0", "credit": "5000"},
        ]
        assert validate_debit_equals_credit(lines) is True

    def test_unbalanced_entry(self) -> None:
        lines = [
            {"debit": "5000", "credit": "0"},
            {"debit": "0", "credit": "4999"},
        ]
        assert validate_debit_equals_credit(lines) is False

    def test_multi_line_balanced(self) -> None:
        lines = [
            {"debit": "1000", "credit": "0"},
            {"debit": "500", "credit": "0"},
            {"debit": "0", "credit": "1500"},
        ]
        assert validate_debit_equals_credit(lines) is True

    def test_empty_lines(self) -> None:
        assert validate_debit_equals_credit([]) is True  # 0 == 0


class TestVatAmount:
    def test_correct_15pct_vat(self) -> None:
        subtotal = Decimal("1000.00")
        vat_rate = Decimal("15")
        vat_amount = Decimal("150.00")
        assert validate_vat_amount(subtotal, vat_rate, vat_amount) is True

    def test_incorrect_vat(self) -> None:
        subtotal = Decimal("1000.00")
        vat_rate = Decimal("15")
        vat_amount = Decimal("140.00")  # wrong
        assert validate_vat_amount(subtotal, vat_rate, vat_amount) is False

    def test_vat_rounding(self) -> None:
        # 333.33 * 15% = 49.9995 → rounds to 50.00
        subtotal = Decimal("333.33")
        vat_rate = Decimal("15")
        vat_amount = Decimal("50.00")
        assert validate_vat_amount(subtotal, vat_rate, vat_amount) is True


class TestNetSalary:
    def test_basic_net(self) -> None:
        assert validate_net_salary(
            basic=Decimal("8000"),
            allowances=Decimal("1000"),
            deductions=Decimal("500"),
            net=Decimal("8500"),
        ) is True

    def test_wrong_net(self) -> None:
        assert validate_net_salary(
            basic=Decimal("8000"),
            allowances=Decimal("1000"),
            deductions=Decimal("500"),
            net=Decimal("9000"),  # wrong
        ) is False


class TestBalanceSheet:
    def test_balanced(self) -> None:
        assert validate_balance_sheet(
            total_assets=Decimal("100000"),
            total_liabilities=Decimal("40000"),
            total_equity=Decimal("60000"),
        ) is True

    def test_unbalanced(self) -> None:
        assert validate_balance_sheet(
            total_assets=Decimal("100000"),
            total_liabilities=Decimal("40000"),
            total_equity=Decimal("55000"),  # wrong
        ) is False
