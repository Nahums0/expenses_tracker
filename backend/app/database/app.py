from flask import Flask
import app.database.models as db_models
from app.logger import log
from alembic.config import Config
from alembic import command

APP_NAME = "DB INIT"

# Get a database connection and run db init script
def initialize_database(flask_app: Flask):
    try:
        db_models.db.init_app(flask_app)

        with flask_app.app_context():
            alembic_cfg = Config("alembic.ini")
            command.upgrade(alembic_cfg, "head")
        log(APP_NAME, "INFO", "Database initialized successfully.")
    except Exception as e:
        log(APP_NAME, "ERROR", f"Database initialization failed: {e}")
        raise e
