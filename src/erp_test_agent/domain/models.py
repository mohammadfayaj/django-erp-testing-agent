"""Domain models for test plans, steps, and run results."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

from erp_test_agent.domain.enums import AssertionType, Priority, RunStatus, StepStatus


@dataclass
class Assertion:
    """A single assertion to validate after a step or plan completes."""

    type: AssertionType
    # Flexible payload – different assertion types use different keys
    params: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Assertion":
        assertion_type = AssertionType(data.pop("type"))
        return cls(type=assertion_type, params=data)


@dataclass
class TestStep:
    """A single atomic business action within a test plan."""

    action: str
    data: dict[str, Any] = field(default_factory=dict)
    assertions: list[Assertion] = field(default_factory=list)
    retry: int = 1
    # Runtime state (populated during execution)
    status: StepStatus = StepStatus.PENDING
    error: str | None = None
    screenshot: Path | None = None
    duration_ms: float = 0.0


@dataclass
class Preconditions:
    """Conditions that must be true before the plan can execute."""

    login_required: bool = True
    company: str | None = None
    fiscal_year: int | None = None
    depends_on: list[str] = field(default_factory=list)


@dataclass
class TestPlan:
    """A complete business test plan loaded from a YAML file."""

    name: str
    department: str
    role: str
    environment: str
    steps: list[TestStep]
    assertions: list[Assertion] = field(default_factory=list)
    preconditions: Preconditions = field(default_factory=Preconditions)
    priority: Priority = Priority.MEDIUM
    # Path to the originating YAML file
    source_path: Path | None = None


@dataclass
class StepResult:
    """Execution result for a single step."""

    step: TestStep
    status: StepStatus
    output: dict[str, Any] = field(default_factory=dict)
    error: str | None = None
    screenshot: Path | None = None
    duration_ms: float = 0.0
    attempt: int = 1


@dataclass
class RunResult:
    """Aggregated result of a full test plan run."""

    run_id: str
    plan: TestPlan
    status: RunStatus = RunStatus.PENDING
    step_results: list[StepResult] = field(default_factory=list)
    started_at: datetime = field(default_factory=datetime.utcnow)
    finished_at: datetime | None = None
    artifact_dir: Path | None = None
    # Context dict shared between steps (stores created record IDs etc.)
    context: dict[str, Any] = field(default_factory=dict)

    @property
    def duration_ms(self) -> float:
        if self.finished_at is None:
            return 0.0
        return (self.finished_at - self.started_at).total_seconds() * 1000

    @property
    def passed(self) -> int:
        return sum(1 for r in self.step_results if r.status == StepStatus.PASSED)

    @property
    def failed(self) -> int:
        return sum(1 for r in self.step_results if r.status == StepStatus.FAILED)
