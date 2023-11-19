# Standard library imports
import calendar
import json
import logging
import os
import uuid
from datetime import datetime, timedelta

# Third-party imports
import bcrypt
import requests
from flask import Flask, jsonify, make_response
from flask_wtf import FlaskForm
from sqlalchemy import and_
from sqlalchemy.orm import joinedload
from sqlalchemy.orm.attributes import InstrumentedAttribute
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, Length

# Local application imports
from app.api.api import register_api_routes
from app.database.app import initialize_database
from app.database.models import User, Transaction, UserWarnings, db
from app.job_scheduler.app import start_scheduler
from config.app import STOP_AT_FAILED_LOGIN_THRESHOLD
from config.logger import LOG_FORMAT, LOG_LEVEL
from lib.jwt.jwt import jwt


# Constants
MIN_PASSWORD_LENGTH = 8
MIN_APP_CREDS_LENGTH = 4
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
PROMPT_TEMPLATE = (
    "Choose the best category for each of the given transactions from the give categories list.\n"
    "- DO NOT MAKE UP CATEGORIES.\n"
    "- DO NOT PROVIDE ANY TEXT OTHER THAN THE EXPECTED OUTPUT.\n"
    "- IF UNCERTAIN, USE THE 'General' CATEGORY.\n"
    "Categories list:\n"
    "{categories_string}.\n"
    "Transactions:\n"
    "{transactions_string}\n"
    "Expected Output:\n"
    '"Category for #{{index_number}}: [chosen_category_1]"\n'
    '"Category for #{{index_number}}: [chosen_category_2]"\n'
    "END OF OUTPUT"
)


# Creata a flask app
def create_app(initialize_db=True, initialize_scheduler=True):
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
    IS_DEBUG = os.environ.get("IS_DEBUG", "TRUE") == "TRUE"
    DATABASE_URI = os.environ.get("DATABASE_URI")

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


# Helper Functions and Classes
def get_prompt_template(categories_string, transactions_string):
    return PROMPT_TEMPLATE.format(categories_string=categories_string, transactions_string=transactions_string)


def setup_werkzeug_logger():
    # TODO: This either gets overriden by other loggers or doesn't change werkzeug at all
    werkzeug_logger = logging.getLogger("werkzeug")
    werkzeug_logger.setLevel(LOG_LEVEL)
    for handler in werkzeug_logger.handlers:
        handler.setFormatter(logging.Formatter(LOG_FORMAT))


def create_response(message, status_code, data=None):
    response_data = {"message": message, "status_code": status_code}
    if data is not None:
        response_data["data"] = data
    return make_response(jsonify(response_data), status_code)


class RegistrationForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=MIN_PASSWORD_LENGTH)])
    inviteKey = StringField("inviteKey", validators=[DataRequired()])


class UserLoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=MIN_PASSWORD_LENGTH)])


def hash_password(password):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode("utf-8"), salt)


def verify_password(input_password, hashed_password):
    return bcrypt.checkpw(input_password.encode("utf-8"), hashed_password)


def calculate_next_recurrence_date(current_date, frequency_value, frequency_unit, start_date):
    if frequency_unit == "days":
        return current_date + datetime.timedelta(days=frequency_value)
    elif frequency_unit == "weeks":
        return current_date + datetime.timedelta(weeks=frequency_value)
    elif frequency_unit == "months":
        month = (current_date.month - 1 + frequency_value) % 12 + 1
        year = current_date.year + (current_date.month - 1 + frequency_value) // 12
        day = min(start_date.day, calendar.monthrange(year, month)[1])
    return datetime(year, month, day)


# Query users who have been flagged for scraping and preload their associated credentials.
def fetch_users_for_scraping():
    users = (
        User.query.options(joinedload(User.appUserCredentials))
        .filter(and_(User.shouldGetScrapped == True, User.initialSetupDone == True))
        .all()
    )
    skipped_users = []

    index = 0
    while index < len(users):
        user = users[index]
        user_warnings = UserWarnings.query.filter(UserWarnings.userEmail == user.email).first()

        # Check if there are any warnings for the user.
        if user_warnings is not None:
            # If the failed login count for the user exceeds the defined threshold,
            # log it and remove the user from the list.

            if user_warnings.failedLoginCount >= STOP_AT_FAILED_LOGIN_THRESHOLD:
                skipped_users.append(user.email)
                users.pop(index)
                continue
        index += 1

    return users, skipped_users


def transform_transactions_for_user(user, transactions):
    transactions_list = []
    for transaction in transactions:
        transformed_transaction = Transaction(
            id=user.email + "_" + transaction["arn"],
            arn=transaction["arn"],
            userEmail=user.email,
            categoryId=0,
            transactionAmount=transaction["transaction_amount"],
            paymentDate=transaction["payment_date"],
            purchaseDate=transaction["purchase_date"],
            shortCardNumber=transaction["short_card_number"],
            merchantData=transaction["merchant_data"],
            originalCurrency=transaction["original_payment"]["currency"],
            originalAmount=transaction["original_payment"]["amount"],
        )
        transactions_list.append(transformed_transaction)
    return transactions_list


def process_recurring_transactions(recurring_transactions):
    """Handle recurring transactions and return a list of transactions to be added."""
    transactions_to_add = []

    for transaction in recurring_transactions:
        recurring_transaction = transaction.recurring_transaction
        current_date = datetime.now()

        if recurring_transaction.scannedAt:
            next_scan_date = calculate_next_recurrence_date(
                recurring_transaction.scannedAt,
                recurring_transaction.frequency_value,
                recurring_transaction.frequency_unit,
                recurring_transaction.startDate,
            )
        else:
            next_scan_date = recurring_transaction.startDate

        while next_scan_date <= current_date:
            column_data = {
                key: getattr(transaction, key)
                for key in dir(transaction)
                if isinstance(getattr(Transaction, key, None), InstrumentedAttribute)
            }

            column_data["id"] = str(uuid.uuid4())
            column_data["arn"] = str(uuid.uuid4())
            column_data["paymentDate"] = next_scan_date
            column_data["purchaseDate"] = next_scan_date
            column_data.pop("recurring_transaction", None)
            column_data.pop("isRecurring", None)

            new_transaction = Transaction(**column_data)
            transactions_to_add.append(new_transaction)

            next_scan_date = calculate_next_recurrence_date(
                next_scan_date,
                recurring_transaction.frequency_value,
                recurring_transaction.frequency_unit,
                recurring_transaction.startDate,
            )
        recurring_transaction.scannedAt = current_date

    return transactions_to_add


def query_chatgpt(prompt):
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {OPENAI_API_KEY}"}
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.1,
    }
    response = requests.post(OPENAI_API_URL, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"Error {response.status_code}: {response.text}"


def add_failed_login_user_warning(user_email):
    user_warning = UserWarnings.query.filter(UserWarnings.userEmail == user_email).first()

    if user_warning is None:
        user_warning = UserWarnings(userEmail=user_email, failedLoginCount=1)
        db.session.add(user_warning)
    else:
        user_warning.failedLoginCount += 1

    db.session.commit()


# Convert a date to a number format (1/11/2023 -> 202311)
def date_to_number(date):
    return date.year * 100 + date.month
