"""Main planner: loads YAML plans, resolves dependencies, compiles steps."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

import yaml

from erp_test_agent.domain.enums import AssertionType, Priority, StepStatus
from erp_test_agent.domain.models import Assertion, Preconditions, TestPlan, TestStep
from erp_test_agent.domain.schemas import TestPlanSchema
from erp_test_agent.planner.dependency_graph import DependencyGraph
from erp_test_agent.planner.step_compiler import StepCompiler
from erp_test_agent.utils.logging import logger


class Planner:
    """Reads, validates, and compiles test plans into an ordered execution list.

    Usage::

        planner = Planner()
        plans = planner.load_plans(["plans/procurement/create_vendor.yaml"])
        ordered = planner.resolve_order(plans)
        compiled = planner.compile(ordered, run_id="run_20260521_001")
    """

    def load_plan(self, path: Path | str) -> TestPlan:
        """Load and validate a single YAML plan file."""
        path = Path(path)
        schema = TestPlanSchema.from_yaml_file(path)
        return self._schema_to_model(schema, source_path=path)

    def load_plans(self, paths: Iterable[Path | str]) -> list[TestPlan]:
        """Load and validate multiple YAML plan files."""
        plans: list[TestPlan] = []
        for p in paths:
            try:
                plan = self.load_plan(p)
                plans.append(plan)
                logger.info(f"Loaded plan: {plan.name} ({p})")
            except Exception as exc:
                logger.error(f"Failed to load plan from {p}: {exc}")
                raise
        return plans

    def resolve_order(self, plans: list[TestPlan]) -> list[TestPlan]:
        """Return plans sorted in dependency-respecting topological order."""
        graph = DependencyGraph(plans)
        ordered = graph.ordered()
        logger.debug(f"Execution order: {[p.name for p in ordered]}")
        return ordered

    def compile(self, plans: list[TestPlan], run_id: str) -> list[TestPlan]:
        """Render template variables in all steps for the given run_id."""
        compiler = StepCompiler(run_id=run_id)
        return [compiler.compile(plan) for plan in plans]

    # ── internal helpers ──────────────────────────────────────────────────────

    @staticmethod
    def _schema_to_model(schema: TestPlanSchema, source_path: Path | None = None) -> TestPlan:
        steps = [
            TestStep(
                action=s.action,
                data=s.data,
                assertions=[
                    Assertion(type=a.type, params=a.model_extra or {})
                    for a in s.assertions
                ],
                retry=s.retry,
            )
            for s in schema.steps
        ]
        assertions = [
            Assertion(type=a.type, params=a.model_extra or {})
            for a in schema.assertions
        ]
        preconditions = Preconditions(
            login_required=schema.preconditions.login_required,
            company=schema.preconditions.company,
            fiscal_year=schema.preconditions.fiscal_year,
            depends_on=schema.preconditions.depends_on,
        )
        return TestPlan(
            name=schema.name,
            department=schema.department,
            role=schema.role,
            environment=schema.environment,
            priority=schema.priority,
            steps=steps,
            assertions=assertions,
            preconditions=preconditions,
            source_path=source_path,
        )
