from datetime import date

from app.streaks import build_weekly_summary, calculate_current_streak


def test_current_streak_two_consecutive_days_including_today() -> None:
    today = date(2026, 4, 9)
    completion_dates = ["2026-04-08", "2026-04-09"]

    assert calculate_current_streak(completion_dates, today=today) == 2


def test_current_streak_is_zero_when_today_missing() -> None:
    today = date(2026, 4, 9)
    completion_dates = ["2026-04-07", "2026-04-08"]

    assert calculate_current_streak(completion_dates, today=today) == 0


def test_current_streak_stops_at_gap() -> None:
    today = date(2026, 4, 9)
    completion_dates = ["2026-04-06", "2026-04-08", "2026-04-09"]

    assert calculate_current_streak(completion_dates, today=today) == 2


def test_current_streak_ignores_duplicates() -> None:
    today = date(2026, 4, 9)
    completion_dates = ["2026-04-08", "2026-04-09", "2026-04-09"]

    assert calculate_current_streak(completion_dates, today=today) == 2


def test_current_streak_empty_history() -> None:
    today = date(2026, 4, 9)

    assert calculate_current_streak([], today=today) == 0


def test_current_streak_ignores_invalid_date_values() -> None:
    today = date(2026, 4, 9)
    completion_dates = ["not-a-date", "2026-04-09", "2026-04-08"]

    assert calculate_current_streak(completion_dates, today=today) == 2


def test_weekly_summary_returns_expected_flags() -> None:
    today = date(2026, 4, 9)
    completion_dates = ["2026-04-07", "2026-04-09"]

    summary = build_weekly_summary(completion_dates, days=3, today=today)

    assert summary == [
        {"date": "2026-04-07", "completed": True},
        {"date": "2026-04-08", "completed": False},
        {"date": "2026-04-09", "completed": True},
    ]

