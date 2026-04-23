"""Flask application factory for the Habit Tracker MVP."""

from __future__ import annotations

import os
from typing import Any

from flask import Flask


def create_app(test_config: dict[str, Any] | None = None) -> Flask:
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "habit-tracker-dev-key")

    if test_config:
        app.config.update(test_config)

    from .routes import bp

    app.register_blueprint(bp)
    return app
