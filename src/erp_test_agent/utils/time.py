"""Utilities: date/time helpers for plan template rendering."""

from datetime import date, timedelta


def today() -> str:
    return date.today().isoformat()


def today_plus(days: int) -> str:
    return (date.today() + timedelta(days=days)).isoformat()


def current_month() -> int:
    return date.today().month


def current_year() -> int:
    return date.today().year


def fiscal_year_start(year: int | None = None) -> str:
    y = year or date.today().year
    return date(y, 1, 1).isoformat()


__all__ = [
    "today",
    "today_plus",
    "current_month",
    "current_year",
    "fiscal_year_start",
]
