from __future__ import annotations

import json
from pathlib import Path
from typing import Any
from uuid import uuid4

Habit = dict[str, Any]


class StorageError(Exception):
    """Raised when habit data cannot be loaded or saved safely."""


def validate_habit_name(name: str) -> str:
    """Validate and return a cleaned habit name."""
    cleaned = (name or "").strip()
    if not cleaned:
        raise ValueError("Habit name cannot be empty.")
    return cleaned


def _normalize_completion_dates(value: Any) -> list[str]:
    """Return a de-duplicated list of non-empty date strings."""
    if not isinstance(value, list):
        return []

    unique_dates: list[str] = []
    seen: set[str] = set()

    for item in value:
        if not isinstance(item, str):
            continue
        cleaned = item.strip()
        if cleaned and cleaned not in seen:
            seen.add(cleaned)
            unique_dates.append(cleaned)

    return unique_dates


def _normalize_habit(raw: Any) -> Habit:
    """Validate one raw habit object from JSON."""
    if not isinstance(raw, dict):
        raise StorageError("Each habit entry must be a JSON object.")

    habit_id = raw.get("id")
    if not isinstance(habit_id, str) or not habit_id.strip():
        raise StorageError("Each habit must include a non-empty string 'id'.")

    name = raw.get("name")
    if not isinstance(name, str) or not name.strip():
        raise StorageError("Each habit must include a non-empty string 'name'.")

    return {
        "id": habit_id.strip(),
        "name": name.strip(),
        "completion_dates": _normalize_completion_dates(raw.get("completion_dates", [])),
    }


def load_habits(file_path: str | Path) -> list[Habit]:
    """Load habits from JSON file; return [] if file is missing or empty."""
    path = Path(file_path)

    if not path.exists():
        return []

    try:
        raw_text = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise StorageError(f"Could not read data file: {exc}") from exc

    if not raw_text.strip():
        return []

    try:
        parsed = json.loads(raw_text)
    except json.JSONDecodeError as exc:
        raise StorageError("Data file is malformed JSON.") from exc

    if not isinstance(parsed, list):
        raise StorageError("Data file must contain a JSON list of habits.")

    return [_normalize_habit(item) for item in parsed]


def save_habits(file_path: str | Path, habits: list[Habit]) -> None:
    """Save habits to JSON file after validation."""
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    normalized_habits = [_normalize_habit(habit) for habit in habits]

    try:
        path.write_text(json.dumps(normalized_habits, indent=2), encoding="utf-8")
    except OSError as exc:
        raise StorageError(f"Could not write data file: {exc}") from exc


def create_habit(name: str) -> Habit:
    """Create a new habit object with a generated id."""
    cleaned_name = validate_habit_name(name)
    return {"id": str(uuid4()), "name": cleaned_name, "completion_dates": []}


def find_habit_by_id(habits: list[Habit], habit_id: str) -> Habit | None:
    """Find one habit by id, or return None."""
    for habit in habits:
        if habit.get("id") == habit_id:
            return habit
    return None


def add_completion_date(habit: Habit, date_str: str) -> bool:
    """Add a completion date once; return False if it already exists."""
    completion_dates = habit.get("completion_dates")
    if not isinstance(completion_dates, list):
        completion_dates = []
        habit["completion_dates"] = completion_dates

    if date_str in completion_dates:
        return False

    completion_dates.append(date_str)
    return True

