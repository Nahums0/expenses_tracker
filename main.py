from datetime import date, timedelta
from flask import Flask
from app.api.api import register_api_routes
from app.database.app import initialize_database
import os
from app.helper import setup_werkzeug_logger
from app.job_scheduler.app import start_scheduler
from config.app import IS_DEBUG, JWT_SECRET_KEY
from config.database import DATABASE_URI
from lib.jwt.jwt import jwt
import dotenv

def create_app(initialize_db=True, initialize_scheduler=True):
    db_uri = os.environ.get("DATABASE_URI", None)
    if db_uri is None:
        if IS_DEBUG:
            # Setup default database uri for debugging purposes
            db_uri = DATABASE_URI
            os.environ["DATABASE_URI"] = db_uri
        else:
            raise Exception("The 'DATABASE_URI' env variable is missing, cannot create the app")

    # Initialize api
    app = Flask(__name__)
    app = register_api_routes(app)
    app.config["JSON_AS_ASCII"] = False
    app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    app.config["WTF_CSRF_ENABLED"] = False
    app.config["JWT_SECRET_KEY"] = JWT_SECRET_KEY
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=1)

    jwt.init_app(app)

    if initialize_db:
        initialize_database(app)

    if initialize_scheduler:
        start_scheduler(app)

    return app


if __name__ == "__main__":
    dotenv.load_dotenv()
    setup_werkzeug_logger()
    app = create_app()
    app.run(debug=False)
