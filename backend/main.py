from app.helper import create_app, setup_werkzeug_logger
import dotenv

if __name__ == "__main__":
    dotenv.load_dotenv()
    setup_werkzeug_logger()
    app = create_app()
    app.run(debug=False)
