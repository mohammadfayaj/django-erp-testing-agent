"""Dependency graph builder for test plans."""

from __future__ import annotations

from collections import defaultdict, deque
from typing import Iterable

import networkx as nx

from erp_test_agent.domain.models import TestPlan
from erp_test_agent.utils.logging import logger


class DependencyGraph:
    """Builds and resolves an execution ordering for a collection of plans.

    Plans declare ``preconditions.depends_on`` listing other plan names that
    must complete before them.  This class constructs a DAG and returns plans
    in topological order.
    """

    def __init__(self, plans: Iterable[TestPlan]) -> None:
        self._plans: dict[str, TestPlan] = {p.name: p for p in plans}
        self._graph = nx.DiGraph()
        self._build()

    def _build(self) -> None:
        for name, plan in self._plans.items():
            self._graph.add_node(name)
            for dep in plan.preconditions.depends_on:
                if dep not in self._plans:
                    logger.warning(
                        f"Plan '{name}' depends on '{dep}' which is not in the current run set."
                    )
                self._graph.add_edge(dep, name)  # dep → name (dep must run first)

    def ordered(self) -> list[TestPlan]:
        """Return plans in topological execution order."""
        try:
            order = list(nx.topological_sort(self._graph))
        except nx.NetworkXUnfeasible as exc:
            raise ValueError(f"Circular dependency detected in test plans: {exc}") from exc
        return [self._plans[name] for name in order if name in self._plans]

    def get_dependencies(self, plan_name: str) -> list[str]:
        """Return direct dependencies of a given plan."""
        return list(self._graph.predecessors(plan_name))

    def get_dependants(self, plan_name: str) -> list[str]:
        """Return plans that directly depend on the given plan."""
        return list(self._graph.successors(plan_name))
