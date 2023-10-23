import calendar
from datetime import datetime
import json
import uuid
from flask import jsonify, make_response
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, Length
import bcrypt
from app.database.models import Category, CategoryMonthlyAveragesHistory, User, Transaction, UserCategoryData, db
from sqlalchemy.orm import joinedload
from sqlalchemy.orm.attributes import InstrumentedAttribute
import os
import openai
import requests

PROMPT_TEMPLATE = """Choose the best category for each of the given transactions:
{categories_string}.
Transactions:
{transactions_string}
* DO NOT PROVIDE ANY TEXT OTHER THAN THE EXPECTED OUTPUT
* ONLY PICK CATEGORIES FROM THE PROVIDEN LIST
Expected Output:
"Category for #{{index_number}}: [chosen_category_1]"
"Category for #{{index_number}}: [chosen_category_2]"
END OF OUTPUT"""

def get_prompt_template(categories_string, transactions_string):
    return PROMPT_TEMPLATE.format(categories_string=categories_string, transactions_string=transactions_string)


def create_response(message, status_code, data=None, json=True):
    response_data = {"message": message, "status_code": status_code}
    if data:
        response_data['data'] = data

    if json:
        response = make_response(jsonify(response_data), status_code)
    else:
        response = make_response(jsonify(response_data), status_code)

    return response


class RegistrationForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8)])
    appUsername = StringField(
        "App Username", validators=[DataRequired(), Length(min=4)]
    )
    appPassword = StringField(
        "App Password", validators=[DataRequired(), Length(min=4)]
    )
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
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8)])


def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password

def verify_password(input_password, hashed_password):
    input_password_bytes = input_password.encode('utf-8')
    return bcrypt.checkpw(input_password_bytes, hashed_password)

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
    """Fetch all users marked for scraping from the database."""
    return User.query.options(joinedload(User.appUserCredentials)).filter_by(shouldGetScrapped=True).all()


def transform_transactions_for_user(user, transactions):
    """Transform raw transaction data to a list of Transaction objects."""
    transactions_list = []
    for transaction in transactions:
        transformed_transaction = Transaction(
            arn=transaction["arn"],
            userEmail=user.email,
            categoryId=0,  # Default categoryId
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


def initiate_category_data(category_id, user_email, db):
    # Create UserCategoryData for the user
    db.session.add(UserCategoryData(
        categoryId=category_id, 
        userEmail=user_email,
        monthlyBudget=-1,
        monthlySpending=0,
        monthlyAverage=0,
        ))


def query_chatgpt(prompt):
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

    url = 'https://api.openai.com/v1/chat/completions'

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {OPENAI_API_KEY}'
    }

    data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.3
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))

    # Check if the request was successful
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"Error {response.status_code}: {response.text}"


