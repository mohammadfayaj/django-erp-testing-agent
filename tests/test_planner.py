"""Tests for the Planner layer."""

from __future__ import annotations

from pathlib import Path

import pytest

from erp_test_agent.domain.enums import Priority
from erp_test_agent.domain.models import Preconditions, TestPlan, TestStep
from erp_test_agent.planner.dependency_graph import DependencyGraph
from erp_test_agent.planner.planner import Planner
from erp_test_agent.planner.step_compiler import StepCompiler


# ── Fixtures ──────────────────────────────────────────────────────────────────

def _make_plan(name: str, depends_on: list[str] | None = None) -> TestPlan:
    return TestPlan(
        name=name,
        department="test",
        role="admin",
        environment="local",
        steps=[
            TestStep(action="navigate", data={"module": "procurement"}),
        ],
        preconditions=Preconditions(depends_on=depends_on or []),
    )


# ── DependencyGraph tests ──────────────────────────────────────────────────────

class TestDependencyGraph:
    def test_single_plan_no_deps(self) -> None:
        plan = _make_plan("plan_a")
        graph = DependencyGraph([plan])
        ordered = graph.ordered()
        assert len(ordered) == 1
        assert ordered[0].name == "plan_a"

    def test_two_plans_in_order(self) -> None:
        plan_a = _make_plan("plan_a")
        plan_b = _make_plan("plan_b", depends_on=["plan_a"])
        graph = DependencyGraph([plan_a, plan_b])
        ordered = graph.ordered()
        names = [p.name for p in ordered]
        assert names.index("plan_a") < names.index("plan_b")

    def test_missing_dependency_is_warned_not_raised(self) -> None:
        plan = _make_plan("plan_z", depends_on=["plan_missing"])
        # Should not raise – missing deps are warned
        graph = DependencyGraph([plan])
        ordered = graph.ordered()
        assert any(p.name == "plan_z" for p in ordered)

    def test_circular_dependency_raises(self) -> None:
        plan_a = _make_plan("plan_a", depends_on=["plan_b"])
        plan_b = _make_plan("plan_b", depends_on=["plan_a"])
        graph = DependencyGraph([plan_a, plan_b])
        with pytest.raises(ValueError, match="Circular dependency"):
            graph.ordered()


# ── StepCompiler tests ─────────────────────────────────────────────────────────

class TestStepCompiler:
    def test_run_id_substitution(self) -> None:
        compiler = StepCompiler(run_id="run_20260521_abc123")
        plan = _make_plan("p")
        plan.steps = [
            TestStep(
                action="create_vendor",
                data={"vendor_name": "Vendor {{ run_id }}"},
            )
        ]
        compiled = compiler.compile(plan)
        assert compiled.steps[0].data["vendor_name"] == "Vendor run_20260521_abc123"

    def test_today_substitution(self) -> None:
        from erp_test_agent.utils.time import today
        compiler = StepCompiler(run_id="run_test_001")
        plan = _make_plan("p")
        plan.steps = [
            TestStep(action="navigate", data={"date": "{{ today }}"})
        ]
        compiled = compiler.compile(plan)
        assert compiled.steps[0].data["date"] == today()

    def test_nested_dict_rendering(self) -> None:
        compiler = StepCompiler(run_id="R001")
        plan = _make_plan("p")
        plan.steps = [
            TestStep(
                action="create_purchase_order",
                data={
                    "items": [{"description": "Item {{ run_id }}", "qty": 5}]
                },
            )
        ]
        compiled = compiler.compile(plan)
        assert compiled.steps[0].data["items"][0]["description"] == "Item R001"

    def test_no_template_vars_unchanged(self) -> None:
        compiler = StepCompiler(run_id="R999")
        plan = _make_plan("p")
        plan.steps = [TestStep(action="login", data={"username": "admin"})]
        compiled = compiler.compile(plan)
        assert compiled.steps[0].data["username"] == "admin"


# ── Planner integration test ──────────────────────────────────────────────────

class TestPlanner:
    def test_load_plan_from_yaml(self, tmp_path: Path) -> None:
        yaml_content = """
name: test_plan_load
department: procurement
role: purchase_manager
environment: local
steps:
  - action: navigate
    data:
      module: procurement
      sub_module: vendors
  - action: create_vendor
    data:
      vendor_name: Test Vendor
      country: SA
"""
        plan_file = tmp_path / "test_plan.yaml"
        plan_file.write_text(yaml_content)

        planner = Planner()
        plan = planner.load_plan(plan_file)

        assert plan.name == "test_plan_load"
        assert plan.department == "procurement"
        assert len(plan.steps) == 2
        assert plan.steps[0].action == "navigate"
        assert plan.steps[1].action == "create_vendor"
        assert plan.steps[1].data["vendor_name"] == "Test Vendor"

    def test_compile_substitutes_run_id(self, tmp_path: Path) -> None:
        yaml_content = """
name: test_compile
department: sales
role: sales_user
environment: local
steps:
  - action: create_customer
    data:
      customer_name: Customer {{ run_id }}
"""
        plan_file = tmp_path / "compile_plan.yaml"
        plan_file.write_text(yaml_content)

        planner = Planner()
        plans = planner.load_plans([plan_file])
        compiled = planner.compile(plans, run_id="TESTRUN01")
        assert "TESTRUN01" in compiled[0].steps[0].data["customer_name"]

    def test_resolve_order_respects_deps(self, tmp_path: Path) -> None:
        yaml_a = """
name: plan_alpha
department: procurement
role: purchase_manager
environment: local
steps:
  - action: navigate
    data: {}
"""
        yaml_b = """
name: plan_beta
department: procurement
role: purchase_manager
environment: local
preconditions:
  depends_on:
    - plan_alpha
steps:
  - action: navigate
    data: {}
"""
        (tmp_path / "alpha.yaml").write_text(yaml_a)
        (tmp_path / "beta.yaml").write_text(yaml_b)

        planner = Planner()
        plans = planner.load_plans([tmp_path / "beta.yaml", tmp_path / "alpha.yaml"])
        ordered = planner.resolve_order(plans)
        names = [p.name for p in ordered]
        assert names.index("plan_alpha") < names.index("plan_beta")
