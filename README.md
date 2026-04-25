# Habit Tracker Web App (Flask + JSON)

This project is a small MVP habit tracker built for the AI-Powered Mini SDLC assignment.
It uses Flask templates for UI and a local JSON file for persistence.

## MVP Features Implemented

- Create habit with non-empty name
- View all habits on a single dashboard
- Edit habit name
- Delete habit
- Mark habit complete for today
- Prevent duplicate completion on the same day
- Calculate current streak (must include today)
- Show 7-day completion summary per habit
- Show success/error feedback messages
- Missing JSON file initializes an empty habit list; malformed JSON shows an error message

ASSUMPTION: Dates are stored in ISO format (`YYYY-MM-DD`).

## Project Structure

```text
run.py
requirements.txt
README.md
data/habits.json
app/
  __init__.py
  routes.py
  storage.py
  streaks.py
  templates/dashboard.html
tests/
  test_routes.py
  test_storage.py
  test_streaks.py
```

## Run Locally

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Start the app:

```bash
python run.py
```

4. Open `http://127.0.0.1:5000/`.

Optional environment variable:

- `SECRET_KEY` (if not set, a local development default is used)

## Run Tests

```bash
pytest
```
