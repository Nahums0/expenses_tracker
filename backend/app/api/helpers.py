from datetime import datetime
from flask_jwt_extended import create_access_token
from app.database.models import User
from app.job_scheduler.jobs_config import scheduled_jobs_dict
from app.job_scheduler.app import SchedulerInstance


def get_user_object(email):
    """Generate a user object"""

    user = User.query.filter(User.email == email).first()
    last_transactions_scan_date = user.lastTransactionsScanDate

    if last_transactions_scan_date is not None:
        last_transactions_scan_date = int(datetime.timestamp(user.lastTransactionsScanDate))

    return {
        "email": email,
        "lastTransactionsScanDate": last_transactions_scan_date,
        "initialSetupDone": user.initialSetupDone,
        "fullName": user.fullName,
        "accessToken": create_access_token(identity=email),
        "currency": user.currency,
        "monthlyBudget": user.monthlyBudget,
    }


def validate_recurring_transaction(transaction):
    """Validate recurring transaction object contains the proper fields"""

    def validate_date(date_str):
        """Validate date format YYYY-MM-DD"""
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    errors = {}

    if not transaction.get("name"):
        errors["name"] = "Name is required."

    try:
        float(transaction.get("amount", 0))
    except ValueError:
        errors["amount"] = "Amount must be a number."

    if transaction.get("frequencyUnit") not in ["days", "weeks", "months"]:
        errors["frequencyUnit"] = "Frequency unit must be 'days', 'weeks', or 'months'."

    try:
        frequency_value = int(transaction.get("frequencyValue", 0))
        if frequency_value <= 0:
            errors["frequencyValue"] = "Frequency value must be a positive integer."
    except ValueError:
        errors["frequencyValue"] = "Frequency value must be an integer."

    if not transaction.get("categoryId"):
        errors["categoryId"] = "Category Id is required."

    start_date = transaction.get("startDate")
    if not validate_date(start_date):
        errors["startDate"] = "Start date must be a valid date in YYYY-MM-DD format."

    return errors


def validate_transaction(data):
    """Validate transaction object contains the proper fields"""

    required_fields = ["transactionId", "categoryId", "transactionAmount", "paymentDate", "purchaseDate", "merchantData"]
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return False, f"Missing fields: {', '.join(missing_fields)}"

    return True, ""


def update_recurring_transaction_fields(recurring_transaction, updated_transaction):
    """
    Update the fields of the recurring transaction with the values from the updated transaction.
    """

    recurring_transaction.transactionName = updated_transaction.get("name")
    recurring_transaction.transaction.transactionAmount = updated_transaction.get("amount")
    recurring_transaction.frequencyValue = updated_transaction.get("frequencyValue")
    recurring_transaction.frequencyUnit = updated_transaction.get("frequencyUnit")
    recurring_transaction.transaction.categoryId = updated_transaction.get("categoryId")

    start_date_str = updated_transaction.get("startDate")
    if start_date_str:
        recurring_transaction.startDate = datetime.strptime(start_date_str, "%Y-%m-%d")


def calculate_chunk_index(index, chunk_size):
    """
    Calculate the chunk index for a given transaction index.
    """

    return 0 if index == 0 else int(index / chunk_size)


def initialize_empty_chunk(chunk_size):
    """
    Initialize an empty chunk with a specified size.
    """

    return [None for _ in range(chunk_size)]


def distribute_transactions_across_chunks(transactions, start_index, total_count, chunk_size):
    """
    Distribute transactions across chunks based on their index.
    """

    # Calculate total number of chunks needed
    total_chunks = (calculate_chunk_index(total_count - 1, chunk_size)) + 1
    chunks = [None for _ in range(total_chunks)]

    # Iterate over transactions and place each in the appropriate chunk
    for i in range(start_index, start_index + len(transactions)):
        current_chunk_index = calculate_chunk_index(i, chunk_size)

        # Initialize chunk if it's empty
        if chunks[current_chunk_index] is None:
            chunks[current_chunk_index] = initialize_empty_chunk(chunk_size)

        # Calculate the index of the transaction within its chunk
        transaction_index_within_chunk = i % chunk_size

        # Place the transaction in the correct chunk and position
        chunks[current_chunk_index][transaction_index_within_chunk] = transactions[i - start_index]

    return chunks


def trigger_user_initial_setup_jobs(user_email):
    chained_jobs = [
        scheduled_jobs_dict["transactions_scanner"],
        scheduled_jobs_dict["transactions_categorizer"],
        scheduled_jobs_dict["monthly_spending_calculator"],
    ]

    custom_args = {
        "transactions_scanner": {"args": {"users_list": [user_email]}},
        "transactions_categorizer": {"args": {"users_list": [user_email]}},
        "monthly_spending_calculator": {"args": {"users_list": [user_email], "deep_scan": True}},
    }
    scheduler = SchedulerInstance.get_instance()
    scheduler.trigger_jobs(chained_jobs, custom_args)