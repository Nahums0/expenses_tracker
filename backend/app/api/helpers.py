from datetime import datetime
from flask_jwt_extended import create_access_token
from app.database.models import User


def get_user_object(email):
    """Generate a user object"""

    user = User.query.filter(User.email == email).first()

    return {
        "email": email,
        "lastTransactionsScanDate": int(datetime.timestamp(user.lastTransactionsScanDate)),
        "initialSetupDone": user.initialSetupDone,
        "fullName": user.fullName,
        "accessToken": create_access_token(identity=email),
        "currency": user.currency,
        "monthlyBudget": user.monthlyBudget,
    }


def validate_recurring_transaction(transaction):
    """Validate that a recurring transaction object contains the proper fields"""

    def validate_date(date_str):
        """Validate date format YYYY-MM-DD"""
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    errors = {}

    # Validate name
    if not transaction.get("name"):
        errors["name"] = "Name is required."

    # Validate amount
    try:
        float(transaction.get("amount", 0))
    except ValueError:
        errors["amount"] = "Amount must be a number."

    # Validate frequency unit
    if transaction.get("frequencyUnit") not in ["days", "weeks", "months"]:
        errors["frequencyUnit"] = "Frequency unit must be 'days', 'weeks', or 'months'."

    # Validate frequency value
    try:
        frequency_value = int(transaction.get("frequencyValue", 0))
        if frequency_value <= 0:
            errors["frequencyValue"] = "Frequency value must be a positive integer."
    except ValueError:
        errors["frequencyValue"] = "Frequency value must be an integer."

    # Validate category
    if not transaction.get("categoryId"):
        errors["categoryId"] = "Category Id is required."

    # Validate start date
    start_date = transaction.get("startDate")
    if not validate_date(start_date):
        errors["startDate"] = "Start date must be a valid date in YYYY-MM-DD format."

    return errors


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
