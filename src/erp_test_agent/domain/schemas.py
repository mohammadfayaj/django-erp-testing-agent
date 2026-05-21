"""Pydantic schemas for YAML plan parsing and validation."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field, model_validator

from erp_test_agent.domain.enums import AssertionType, Priority


class AssertionSchema(BaseModel):
    type: AssertionType
    model_config = {"extra": "allow"}

    @model_validator(mode="before")
    @classmethod
    def capture_extra(cls, values: dict[str, Any]) -> dict[str, Any]:
        return values


class StepSchema(BaseModel):
    action: str
    data: dict[str, Any] = Field(default_factory=dict)
    assertions: list[AssertionSchema] = Field(default_factory=list)
    retry: int = 1
    target: str | None = None
    expected_status: str | None = None


class PreconditionsSchema(BaseModel):
    login_required: bool = True
    company: str | None = None
    fiscal_year: int | None = None
    depends_on: list[str] = Field(default_factory=list)


class TestPlanSchema(BaseModel):
    name: str
    department: str
    role: str
    environment: str
    priority: Priority = Priority.MEDIUM
    preconditions: PreconditionsSchema = Field(default_factory=PreconditionsSchema)
    steps: list[StepSchema]
    assertions: list[AssertionSchema] = Field(default_factory=list)

    @classmethod
    def from_yaml_file(cls, path: Path) -> "TestPlanSchema":
        import yaml

        with open(path) as fh:
            data = yaml.safe_load(fh)
        return cls.model_validate(data)
