from __future__ import annotations

from pathlib import Path
from typing import Any

from flask import Blueprint, flash, redirect, render_template, request, url_for

from .storage import (
    StorageError,
    add_completion_date,
    create_habit,
    find_habit_by_id,
    load_habits,
    save_habits,
    validate_habit_name,
)
from .streaks import build_weekly_summary, calculate_current_streak, get_today_iso

bp = Blueprint("habits", __name__)
DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "habits.json"


def _load_habits_or_none() -> list[dict[str, Any]] | None:
    """Load habits and return None if storage is invalid."""
    try:
        return load_habits(DATA_FILE)
    except StorageError as exc:
        flash(f"Could not load habits: {exc}", "error")
        return None


def _save_habits_with_feedback(habits: list[dict[str, Any]]) -> bool:
    """Save habits and return whether save succeeded."""
    try:
        save_habits(DATA_FILE, habits)
        return True
    except StorageError as exc:
        flash(f"Could not save habits: {exc}", "error")
        return False


def _build_dashboard_rows(habits: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Build display data for the dashboard."""
    today = get_today_iso()
    rows: list[dict[str, Any]] = []

    for habit in habits:
        completion_dates = habit.get("completion_dates", [])
        if not isinstance(completion_dates, list):
            completion_dates = []

        rows.append(
            {
                "id": habit.get("id", ""),
                "name": habit.get("name", ""),
                "streak": calculate_current_streak(completion_dates),
                "completed_today": today in completion_dates,
                "weekly_summary": build_weekly_summary(completion_dates, days=7),
            }
        )

    return rows


@bp.get("/")
def dashboard() -> str:
    """Show dashboard with habits, streaks, and weekly summary."""
    habits = _load_habits_or_none()
    if habits is None:
        habits = []
    return render_template(
        "dashboard.html",
        habits=_build_dashboard_rows(habits),
        today=get_today_iso(),
    )


@bp.post("/habits")
def add_habit() -> Any:
    """Create a new habit from form input."""
    name = request.form.get("name", "")

    try:
        new_habit = create_habit(name)
    except ValueError as exc:
        flash(str(exc), "error")
        return redirect(url_for("habits.dashboard"))

    habits = _load_habits_or_none()
    if habits is None:
        return redirect(url_for("habits.dashboard"))
    habits.append(new_habit)

    if _save_habits_with_feedback(habits):
        flash("Habit created.", "success")

    return redirect(url_for("habits.dashboard"))


@bp.post("/habits/<habit_id>/edit")
def edit_habit(habit_id: str) -> Any:
    """Update an existing habit name."""
    name = request.form.get("name", "")

    try:
        cleaned_name = validate_habit_name(name)
    except ValueError as exc:
        flash(str(exc), "error")
        return redirect(url_for("habits.dashboard"))

    habits = _load_habits_or_none()
    if habits is None:
        return redirect(url_for("habits.dashboard"))
    habit = find_habit_by_id(habits, habit_id)
    if habit is None:
        flash("Habit not found.", "error")
        return redirect(url_for("habits.dashboard"))

    habit["name"] = cleaned_name
    if _save_habits_with_feedback(habits):
        flash("Habit updated.", "success")

    return redirect(url_for("habits.dashboard"))


@bp.post("/habits/<habit_id>/complete")
def complete_habit(habit_id: str) -> Any:
    """Mark a habit as completed for today."""
    habits = _load_habits_or_none()
    if habits is None:
        return redirect(url_for("habits.dashboard"))
    habit = find_habit_by_id(habits, habit_id)
    if habit is None:
        flash("Habit not found.", "error")
        return redirect(url_for("habits.dashboard"))

    today = get_today_iso()
    added = add_completion_date(habit, today)
    if not added:
        flash("Habit already completed for today.", "error")
        return redirect(url_for("habits.dashboard"))

    if _save_habits_with_feedback(habits):
        flash("Habit marked as completed today.", "success")

    return redirect(url_for("habits.dashboard"))


@bp.post("/habits/<habit_id>/delete")
def delete_habit(habit_id: str) -> Any:
    """Delete a habit by id."""
    habits = _load_habits_or_none()
    if habits is None:
        return redirect(url_for("habits.dashboard"))
    existing = find_habit_by_id(habits, habit_id)
    if existing is None:
        flash("Habit not found.", "error")
        return redirect(url_for("habits.dashboard"))

    updated_habits = [habit for habit in habits if habit.get("id") != habit_id]
    if _save_habits_with_feedback(updated_habits):
        flash("Habit deleted.", "success")

    return redirect(url_for("habits.dashboard"))
