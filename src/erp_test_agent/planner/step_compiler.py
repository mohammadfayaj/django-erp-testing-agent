"""Step compiler: expands business-level steps into executable atomic actions."""

from __future__ import annotations

from datetime import date, timedelta
from typing import Any

from erp_test_agent.domain.models import TestPlan, TestStep
from erp_test_agent.utils.ids import generate_run_id, make_unique_name
from erp_test_agent.utils.time import current_month, current_year, fiscal_year_start, today


class StepCompiler:
    """Renders template variables inside step data and expands meta-actions.

    Template variables (e.g. ``{{ run_id }}``, ``{{ today }}``) inside YAML
    plan data fields are resolved at compile-time, before execution starts.
    """

    _TEMPLATE_VARS: dict[str, Any]

    def __init__(self, run_id: str) -> None:
        self._run_id = run_id
        today_str = date.today().isoformat()
        self._vars: dict[str, Any] = {
            "run_id": run_id,
            "run_id_numeric": run_id.split("_")[-1],
            "today": today_str,
            "today_plus_7": (date.today() + timedelta(days=7)).isoformat(),
            "today_plus_30": (date.today() + timedelta(days=30)).isoformat(),
            "current_month": current_month(),
            "current_year": current_year(),
            "fiscal_year_start": fiscal_year_start(),
        }

    def compile(self, plan: TestPlan) -> TestPlan:
        """Return a copy of *plan* with all template variables resolved."""
        compiled_steps = [self._compile_step(step) for step in plan.steps]
        # Return a shallow copy with compiled steps
        from dataclasses import replace

        return replace(plan, steps=compiled_steps)

    def _compile_step(self, step: TestStep) -> TestStep:
        from dataclasses import replace

        compiled_data = self._render_dict(step.data)
        return replace(step, data=compiled_data)

    def _render_dict(self, obj: Any) -> Any:
        if isinstance(obj, str):
            return self._render_str(obj)
        if isinstance(obj, dict):
            return {k: self._render_dict(v) for k, v in obj.items()}
        if isinstance(obj, list):
            return [self._render_dict(item) for item in obj]
        return obj

    def _render_str(self, template: str) -> str:
        result = template
        for key, value in self._vars.items():
            result = result.replace("{{ " + key + " }}", str(value))
            result = result.replace("{{" + key + "}}", str(value))
        return result
