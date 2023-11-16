from app.database.models import CategoryMonthlyAveragesHistory, User, db
from app.logger import log

APP_NAME = "Monthly Averages Calculator"

def monthly_averages_calculator(scheduler):
    """Main function to calculate monthly averages."""

    log(APP_NAME, "INFO", "Starting monthly averages calculator")
    with scheduler.flask_app.app_context():
        aggregate_monthly_averages()
    log(APP_NAME, "INFO", "Finished monthly averages calculator")


def aggregate_monthly_averages():
    """Aggregate monthly averages for each category (TODO)."""
    
    users = User.query.all()
    log(APP_NAME, "DEBUG", f"Processing monthly averages for {len(users)} users")
    averages = CategoryMonthlyAveragesHistory.query.all()
