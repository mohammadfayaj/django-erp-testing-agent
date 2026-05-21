"""Utilities: unique ID generation."""

import uuid
from datetime import datetime


def generate_run_id() -> str:
    """Generate a human-readable run ID based on date and a short UUID suffix."""
    ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    suffix = uuid.uuid4().hex[:6]
    return f"run_{ts}_{suffix}"


def generate_step_id(run_id: str, step_index: int) -> str:
    """Generate a step ID scoped to a run."""
    return f"{run_id}_step_{step_index:03d}"


def make_unique_name(prefix: str) -> str:
    """Create a unique name suitable for test data (idempotency-safe)."""
    ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    return f"{prefix}_{ts}"


__all__ = ["generate_run_id", "generate_step_id", "make_unique_name"]
