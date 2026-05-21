"""CLI entry point for the ERP Test Agent.

Usage examples::

    # Run a single plan
    python -m erp_test_agent run plans/procurement/create_vendor.yaml

    # Run with explicit options
    python -m erp_test_agent run plans/procurement/create_vendor.yaml \\
        --env staging --headless --base-url http://staging:8000

    # Run a whole department's plans
    python -m erp_test_agent run-department procurement
"""

from __future__ import annotations

import asyncio
from pathlib import Path

import click
from rich.console import Console
from rich.table import Table

from erp_test_agent.orchestration.workflow_engine import WorkflowEngine
from erp_test_agent.utils.logging import configure_logging
from erp_test_agent.utils.ids import generate_run_id

console = Console()


@click.group()
@click.option("--log-level", default="INFO", show_default=True, help="Logging level")
def main(log_level: str) -> None:
    """ERP Test Agent – agentic ERP testing with Playwright."""
    configure_logging(level=log_level)


@main.command("run")
@click.argument("plan_paths", nargs=-1, required=True, type=click.Path(exists=True))
@click.option("--base-url", envvar="ERP_BASE_URL", default="http://localhost:8000", show_default=True)
@click.option("--username", envvar="ERP_ADMIN_USER", default="admin", show_default=True)
@click.option("--password", envvar="ERP_ADMIN_PASSWORD", default="", show_default=False)
@click.option("--headless/--no-headless", default=True, show_default=True)
@click.option("--slow-mo", default=0, show_default=True, help="ms between browser actions")
@click.option("--browser", default="chromium", type=click.Choice(["chromium", "firefox", "webkit"]))
@click.option("--artifact-dir", default="./artifacts", show_default=True)
def run_plans(
    plan_paths: tuple[str, ...],
    base_url: str,
    username: str,
    password: str,
    headless: bool,
    slow_mo: int,
    browser: str,
    artifact_dir: str,
) -> None:
    """Execute one or more YAML test plans."""
    role_context = {
        "base_url": base_url,
        "username": username,
        "password": password,
    }
    engine = WorkflowEngine(
        artifact_dir=artifact_dir,
        headless=headless,
        slow_mo=slow_mo,
        browser_type=browser,
    )

    run_id = generate_run_id()
    console.print(f"[bold cyan]▶ Run ID:[/bold cyan] {run_id}")

    results = asyncio.run(
        engine.run_workflow(
            list(plan_paths),
            role_context=role_context,
            run_id=run_id,
        )
    )

    # Summary table
    table = Table(title="Run Summary", show_lines=True)
    table.add_column("Plan", style="cyan")
    table.add_column("Status")
    table.add_column("Passed", justify="right")
    table.add_column("Failed", justify="right")
    table.add_column("Duration (ms)", justify="right")

    for r in results:
        status_style = "green" if r.status.value == "passed" else "red"
        table.add_row(
            r.plan.name,
            f"[{status_style}]{r.status.value.upper()}[/{status_style}]",
            str(r.passed),
            str(r.failed),
            f"{r.duration_ms:.0f}",
        )
    console.print(table)


@main.command("run-department")
@click.argument("department")
@click.option("--plans-dir", default="./plans", show_default=True)
@click.option("--base-url", envvar="ERP_BASE_URL", default="http://localhost:8000")
@click.option("--username", envvar="ERP_ADMIN_USER", default="admin")
@click.option("--password", envvar="ERP_ADMIN_PASSWORD", default="")
@click.option("--headless/--no-headless", default=True)
@click.option("--artifact-dir", default="./artifacts", show_default=True)
def run_department(
    department: str,
    plans_dir: str,
    base_url: str,
    username: str,
    password: str,
    headless: bool,
    artifact_dir: str,
) -> None:
    """Execute all plans in a department folder."""
    dept_dir = Path(plans_dir) / department
    if not dept_dir.exists():
        console.print(f"[red]Department folder not found: {dept_dir}[/red]")
        raise SystemExit(1)

    plan_files = sorted(dept_dir.glob("*.yaml"))
    if not plan_files:
        console.print(f"[yellow]No YAML plans found in {dept_dir}[/yellow]")
        return

    console.print(f"[bold]Running {len(plan_files)} plans for department: {department}[/bold]")

    role_context = {"base_url": base_url, "username": username, "password": password}
    engine = WorkflowEngine(artifact_dir=artifact_dir, headless=headless)
    run_id = generate_run_id()

    results = asyncio.run(
        engine.run_workflow(
            [str(p) for p in plan_files],
            role_context=role_context,
            run_id=run_id,
        )
    )

    passed = sum(1 for r in results if r.status.value == "passed")
    failed = len(results) - passed
    console.print(
        f"\n[bold]Department {department}:[/bold] "
        f"[green]{passed} passed[/green] / [red]{failed} failed[/red]"
    )
