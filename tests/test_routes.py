from __future__ import annotations

from pathlib import Path

import pytest

import app.routes as routes_module
from app import create_app
from app.storage import create_habit, load_habits, save_habits
from app.streaks import get_today_iso


@pytest.fixture
def client_and_data_file(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    data_file = tmp_path / "habits.json"
    monkeypatch.setattr(routes_module, "DATA_FILE", data_file)

    app = create_app({"TESTING": True, "SECRET_KEY": "test-secret"})
    with app.test_client() as client:
        yield client, data_file


def test_create_habit_success(client_and_data_file) -> None:
    client, data_file = client_and_data_file

    response = client.post("/habits", data={"name": "Read"}, follow_redirects=True)

    assert response.status_code == 200
    assert b"Habit created." in response.data
    habits = load_habits(data_file)
    assert len(habits) == 1
    assert habits[0]["name"] == "Read"


def test_create_habit_failure_empty_name(client_and_data_file) -> None:
    client, data_file = client_and_data_file

    response = client.post("/habits", data={"name": "   "}, follow_redirects=True)

    assert response.status_code == 200
    assert b"Habit name cannot be empty." in response.data
    assert load_habits(data_file) == []


def test_edit_habit_success(client_and_data_file) -> None:
    client, data_file = client_and_data_file
    habit = create_habit("Old Name")
    save_habits(data_file, [habit])

    response = client.post(
        f"/habits/{habit['id']}/edit",
        data={"name": "New Name"},
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Habit updated." in response.data
    habits = load_habits(data_file)
    assert habits[0]["name"] == "New Name"


def test_edit_habit_failure_empty_name(client_and_data_file) -> None:
    client, data_file = client_and_data_file
    habit = create_habit("Keep Name")
    save_habits(data_file, [habit])

    response = client.post(
        f"/habits/{habit['id']}/edit",
        data={"name": ""},
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Habit name cannot be empty." in response.data
    habits = load_habits(data_file)
    assert habits[0]["name"] == "Keep Name"


def test_edit_habit_rejects_nonexistent_id(client_and_data_file) -> None:
    client, data_file = client_and_data_file
    habit = create_habit("Existing Habit")
    save_habits(data_file, [habit])

    response = client.post(
        "/habits/does-not-exist/edit",
        data={"name": "Updated"},
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Habit not found." in response.data
    habits = load_habits(data_file)
    assert len(habits) == 1
    assert habits[0]["name"] == "Existing Habit"


def test_delete_habit(client_and_data_file) -> None:
    client, data_file = client_and_data_file
    habit = create_habit("To Delete")
    save_habits(data_file, [habit])

    response = client.post(f"/habits/{habit['id']}/delete", follow_redirects=True)

    assert response.status_code == 200
    assert b"Habit deleted." in response.data
    assert load_habits(data_file) == []


def test_delete_habit_rejects_nonexistent_id(client_and_data_file) -> None:
    client, data_file = client_and_data_file
    habit = create_habit("Keep Me")
    save_habits(data_file, [habit])

    response = client.post("/habits/does-not-exist/delete", follow_redirects=True)

    assert response.status_code == 200
    assert b"Habit not found." in response.data
    habits = load_habits(data_file)
    assert len(habits) == 1
    assert habits[0]["id"] == habit["id"]


def test_complete_habit_marks_today(client_and_data_file) -> None:
    client, data_file = client_and_data_file
    habit = create_habit("Complete Me")
    save_habits(data_file, [habit])

    response = client.post(f"/habits/{habit['id']}/complete", follow_redirects=True)

    assert response.status_code == 200
    assert b"Habit marked as completed today." in response.data
    habits = load_habits(data_file)
    assert habits[0]["completion_dates"] == [get_today_iso()]


def test_complete_habit_rejects_nonexistent_id(client_and_data_file) -> None:
    client, data_file = client_and_data_file
    habit = create_habit("Still There")
    save_habits(data_file, [habit])

    response = client.post("/habits/does-not-exist/complete", follow_redirects=True)

    assert response.status_code == 200
    assert b"Habit not found." in response.data
    habits = load_habits(data_file)
    assert len(habits) == 1
    assert habits[0]["completion_dates"] == []


def test_duplicate_completion_rejected(client_and_data_file) -> None:
    client, data_file = client_and_data_file
    habit = create_habit("No Duplicate")
    habit["completion_dates"] = [get_today_iso()]
    save_habits(data_file, [habit])

    response = client.post(f"/habits/{habit['id']}/complete", follow_redirects=True)

    assert response.status_code == 200
    assert b"Habit already completed for today." in response.data
    habits = load_habits(data_file)
    assert habits[0]["completion_dates"] == [get_today_iso()]


def test_dashboard_shows_error_for_malformed_json(client_and_data_file) -> None:
    client, data_file = client_and_data_file
    data_file.write_text("{bad json", encoding="utf-8")

    response = client.get("/", follow_redirects=True)

    assert response.status_code == 200
    assert b"Could not load habits: Data file is malformed JSON." in response.data
