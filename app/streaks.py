from __future__ import annotations

from datetime import date, timedelta
from typing import Iterable


def get_today_iso() -> str:
    """Return today's date as YYYY-MM-DD."""
    return date.today().isoformat()


def parse_iso_date(value: str) -> date | None:
    """Parse YYYY-MM-DD and return None for invalid values."""
    try:
        return date.fromisoformat(value)
    except (TypeError, ValueError):
        return None


def _valid_date_set(completion_dates: Iterable[str]) -> set[date]:
    """Convert date strings to a set of valid date objects."""
    results: set[date] = set()
    for raw in completion_dates:
        parsed = parse_iso_date(raw)
        if parsed is not None:
            results.add(parsed)
    return results


def calculate_current_streak(
    completion_dates: Iterable[str], today: date | None = None
) -> int:
    """
    Calculate the current streak including today.

    Rule: if today is not completed, streak is 0.
    """
    current_day = today or date.today()
    completed_days = _valid_date_set(completion_dates)

    if current_day not in completed_days:
        return 0

    streak = 1
    check_day = current_day

    while True:
        previous_day = check_day - timedelta(days=1)
        if previous_day in completed_days:
            streak += 1
            check_day = previous_day
        else:
            break

    return streak


def get_last_n_days(days: int = 7, today: date | None = None) -> list[date]:
    """Return the last N calendar days, ordered oldest to newest."""
    if days <= 0:
        return []

    anchor = today or date.today()
    start = anchor - timedelta(days=days - 1)
    return [start + timedelta(days=offset) for offset in range(days)]


def build_weekly_summary(
    completion_dates: Iterable[str], days: int = 7, today: date | None = None
) -> list[dict[str, object]]:
    """Build summary rows: [{'date': 'YYYY-MM-DD', 'completed': bool}, ...]."""
    completed_days = _valid_date_set(completion_dates)
    summary: list[dict[str, object]] = []

    for day in get_last_n_days(days=days, today=today):
        summary.append({"date": day.isoformat(), "completed": day in completed_days})

    return summary

