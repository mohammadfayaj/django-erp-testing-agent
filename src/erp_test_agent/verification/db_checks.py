"""Database checks: validate records using a read-only DSN."""

from __future__ import annotations

from typing import Any

from erp_test_agent.utils.logging import logger


async def record_exists_db(dsn: str, table: str, filters: dict[str, Any]) -> bool:
    """Check whether a row matching *filters* exists in *table*.

    This is a stub.  Wire up a real async DB driver (e.g. asyncpg) when a
    ``db_verify_dsn`` is configured in the environment.
    """
    logger.debug(f"[db_check] SELECT 1 FROM {table} WHERE {filters} (DSN configured)")
    # Implement with asyncpg / databases when available
    raise NotImplementedError(
        "db_checks requires a real DB driver; set DB_VERIFY_DSN and implement accordingly."
    )
