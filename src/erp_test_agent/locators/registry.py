"""Central locator registry.

Each module's locators are registered here.  The registry can be used by the
action dispatcher and the recovery agent to look up the correct selector for a
given semantic element.
"""

from __future__ import annotations

from erp_test_agent.locators.accounting import AccountingLocators
from erp_test_agent.locators.hr import HRLocators
from erp_test_agent.locators.payroll import PayrollLocators
from erp_test_agent.locators.procurement import ProcurementLocators
from erp_test_agent.locators.sales import SalesLocators


class LocatorRegistry:
    """Provides a unified interface to module-specific locator classes."""

    procurement = ProcurementLocators
    sales = SalesLocators
    hr = HRLocators
    payroll = PayrollLocators
    accounting = AccountingLocators

    @classmethod
    def get(cls, module: str, element: str) -> str | None:
        """Look up a locator by module name and element name."""
        module_cls = {
            "procurement": cls.procurement,
            "sales": cls.sales,
            "hr": cls.hr,
            "payroll": cls.payroll,
            "accounting": cls.accounting,
        }.get(module)
        if module_cls is None:
            return None
        return getattr(module_cls, element.upper(), None)
