import calendar
import logging
import os
import json
import uuid
from datetime import datetime

import bcrypt
import openai
import requests
from flask import jsonify, make_response
from flask_wtf import FlaskForm
from sqlalchemy.orm import joinedload
from sqlalchemy.orm.attributes import InstrumentedAttribute
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, Length

from app.database.models import User,Transaction, UserCategoryData, db
from config.logger import LOG_FORMAT, LOG_LEVEL

# Constants
MIN_PASSWORD_LENGTH = 8
MIN_APP_CREDS_LENGTH = 4
OPENAI_API_URL = 'https://api.openai.com/v1/chat/completions'
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
    "\"Category for #{{index_number}}: [chosen_category_1]\"\n"
    "\"Category for #{{index_number}}: [chosen_category_2]\"\n"
    "END OF OUTPUT"
)

# Helper Functions and Classes
def get_prompt_template(categories_string, transactions_string):
    return PROMPT_TEMPLATE.format(categories_string=categories_string, transactions_string=transactions_string)

def setup_werkzeug_logger():
    #TODO: This either gets overriden by other loggers or doesn't change werkzeug at all 
    werkzeug_logger = logging.getLogger('werkzeug')
    werkzeug_logger.setLevel(LOG_LEVEL)
    for handler in werkzeug_logger.handlers:
        handler.setFormatter(logging.Formatter(LOG_FORMAT))

def create_response(message, status_code, data=None):
    response_data = {"message": message, "status_code": status_code}
    if data:
        response_data['data'] = data
    return make_response(jsonify(response_data), status_code)

class RegistrationForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=MIN_PASSWORD_LENGTH)])
    appUsername = StringField("App Username", validators=[DataRequired(), Length(min=MIN_APP_CREDS_LENGTH)])
    appPassword = StringField("App Password", validators=[DataRequired(), Length(min=MIN_APP_CREDS_LENGTH)])
    appIdentityDocumentNumber = StringField(
        "App Identity Document Number",
        validators=[
            DataRequired(),
            Length(min=9, max=10),
            lambda form, field: field.data.isdigit(),
        ],
    )

class UserLoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=MIN_PASSWORD_LENGTH)])

def hash_password(password):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt)

def verify_password(input_password, hashed_password):
    return bcrypt.checkpw(input_password.encode('utf-8'), hashed_password)

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

def fetch_users_for_scraping():
    return User.query.options(joinedload(User.appUserCredentials)).filter_by(shouldGetScrapped=True).all()

def transform_transactions_for_user(user, transactions):
    transactions_list = []
    for transaction in transactions:
        transformed_transaction = Transaction(
            id=user.email + "_" + transaction["arn"],
            arn=transaction["arn"],
            userEmail=user.email,
            categoryId=0,
            transactionAmount=transaction['transaction_amount'],
            paymentDate=transaction['payment_date'],
            purchaseDate=transaction['purchase_date'],
            shortCardNumber=transaction['short_card_number'],
            merchantData=transaction['merchant_data'],
            originalCurrency=transaction['original_payment']['currency'],
            originalAmount=transaction['original_payment']['amount']
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
            next_scan_date = calculate_next_recurrence_date(recurring_transaction.scannedAt, recurring_transaction.frequency_value, recurring_transaction.frequency_unit, recurring_transaction.startDate)
        else:
            next_scan_date = recurring_transaction.startDate

        while next_scan_date <= current_date:
            column_data = {key: getattr(transaction, key) for key in dir(transaction)
                           if isinstance(getattr(Transaction, key, None), InstrumentedAttribute)}

            column_data['id'] = str(uuid.uuid4())
            column_data['arn'] = str(uuid.uuid4())
            column_data['paymentDate'] = next_scan_date
            column_data['purchaseDate'] = next_scan_date
            column_data.pop('recurring_transaction', None)
            column_data.pop('isRecurring', None)

            new_transaction = Transaction(**column_data)
            transactions_to_add.append(new_transaction)

            next_scan_date = calculate_next_recurrence_date(next_scan_date, recurring_transaction.frequency_value, recurring_transaction.frequency_unit, recurring_transaction.startDate)
        recurring_transaction.scannedAt = current_date

    return transactions_to_add

def initiate_category_data(category_id, user_email):
    db.session.add(UserCategoryData(
        categoryId=category_id,
        userEmail=user_email,
        monthlyBudget=-1,
        monthlySpending=0,
        monthlyAverage=0,
    ))

def query_chatgpt(prompt):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {OPENAI_API_KEY}'
    }
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
