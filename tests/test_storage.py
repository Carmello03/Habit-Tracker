from datetime import date
from pathlib import Path

import pytest

from app.storage import (
    StorageError,
    add_completion_date,
    create_habit,
    find_habit_by_id,
    load_habits,
    save_habits,
)
from app.streaks import calculate_current_streak


def test_create_save_reload_habit_flow(tmp_path: Path) -> None:
    data_file = tmp_path / "habits.json"
    today = date(2026, 4, 9)
    today_str = today.isoformat()

    habit = create_habit("Read 20 minutes")
    added = add_completion_date(habit, today_str)
    assert added is True

    save_habits(data_file, [habit])
    loaded_habits = load_habits(data_file)

    assert len(loaded_habits) == 1
    reloaded_habit = find_habit_by_id(loaded_habits, habit["id"])
    assert reloaded_habit is not None
    assert reloaded_habit["name"] == "Read 20 minutes"
    assert reloaded_habit["completion_dates"] == [today_str]

    streak = calculate_current_streak(reloaded_habit["completion_dates"], today=today)
    assert streak == 1


def test_load_habits_returns_empty_list_for_missing_file(tmp_path: Path) -> None:
    missing_file = tmp_path / "missing.json"

    assert load_habits(missing_file) == []


def test_load_habits_raises_for_malformed_json(tmp_path: Path) -> None:
    bad_file = tmp_path / "bad.json"
    bad_file.write_text("{not-valid-json", encoding="utf-8")

    with pytest.raises(StorageError):
        load_habits(bad_file)


def test_save_then_reload_deduplicates_completion_dates(tmp_path: Path) -> None:
    data_file = tmp_path / "habits.json"
    habit = {
        "id": "habit-1",
        "name": "Workout",
        "completion_dates": ["2026-04-09", "2026-04-09", "2026-04-08"],
    }

    save_habits(data_file, [habit])
    loaded_habits = load_habits(data_file)

    assert loaded_habits[0]["completion_dates"] == ["2026-04-09", "2026-04-08"]

