import datetime
from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from sqlalchemy import and_
from app.database.models import RecurringTransactions, Transaction, UserCategory, UserCategorySpending, db
from app.helper import create_response
from app.logger import log
from app.api.helpers import (
    distribute_transactions_across_chunks,
    update_recurring_transaction_fields,
    validate_recurring_transaction,
)
from config.app import MAX_TRANSACTIONS_PER_REQUEST, TRANSACTIONS_CHUNK_SIZE
import uuid


APP_NAME = "Transactions Controller"
transactions_bp = Blueprint("transactions", __name__, url_prefix="/api/transactions")


# Define the route for manually adding a transaction
@transactions_bp.route("/add", methods=["POST"])
@jwt_required()
def add_transaction():
    """
    Add a new transaction.
    """
    # TODO: Implement transaction addition logic
    pass


# Define the route for manually deleting a transaction
@transactions_bp.route("/delete", methods=["POST"])
@jwt_required()
def delete_transaction():
    """
    Delete an existing transaction.
    """
    # TODO: Implement transaction deletion logic
    pass


# Define the route for retrieving a user's transactions
@transactions_bp.route("/list", methods=["GET"])
@jwt_required()
def list_transactions():
    """
    List transactions for a user, starting from a given index.
    """
    email = get_jwt_identity()
    num_transactions = request.args.get("length", default=25, type=int)
    start_index = request.args.get("index", default=0, type=int)

    if num_transactions > MAX_TRANSACTIONS_PER_REQUEST:
        return create_response("Request too large", 400)

    try:
        # Count the total number of transactions owned by the user
        total_transactions_count = Transaction.query.filter_by(userEmail=email, isRecurring=False).count()

        # Fetch transaction belonging to the user
        transactions_query = Transaction.query.filter_by(userEmail=email, isRecurring=False).order_by(
            Transaction.purchaseDate.desc()
        )
        transactions = transactions_query.offset(start_index).limit(num_transactions).all()

        # Serialize the transactions to send as a JSON response
        transactions_data = [transaction.serialize() for transaction in transactions]

        # Seperate transactions by chunks
        distributed_transactions = distribute_transactions_across_chunks(
            transactions_data,
            start_index,
            total_transactions_count,
            TRANSACTIONS_CHUNK_SIZE,
        )

        response_body = {
            "transactions": distributed_transactions,
            "chunkSize": TRANSACTIONS_CHUNK_SIZE,
            "totalTransactionsCount": total_transactions_count,
        }

        return create_response("Successfully fetched transactions", 200, response_body)
    except Exception as e:
        log(APP_NAME, "ERROR", f"Error fetching transactions for email: {email}, error: {str(e)}")
        return create_response("An error occurred while fetching transactions", 500)


@transactions_bp.route("/list-recurring-transactions", methods=["GET"])
@jwt_required()
def list_recurring_transactions():
    email = get_jwt_identity()

    try:
        recurring_transactions = RecurringTransactions.query.filter_by(userEmail=email)
        transactions_data = [transaction.serialize() for transaction in recurring_transactions]

        return create_response("Successfully fetched recurring transactions", 200, transactions_data)
    except Exception as e:
        log(APP_NAME, "ERROR", f"Error fetching recurring transactions for email: {email}, error: {str(e)}")
        return create_response("An error occurred while fetching recurring transactions", 500)


@transactions_bp.route("/update-recurring-transaction", methods=["POST"])
@jwt_required()
def update_recurring_transaction():
    """
    Update an existing transaction.
    """
    email = get_jwt_identity()

    try:
        updated_transaction = request.get_json()

        # Validates the data against predefined rules
        validation_errors = validate_recurring_transaction(updated_transaction)
        if validation_errors:
            return create_response("Object validation failed", 400, {"errors": validation_errors})

        # Verify provided category exists and belongs to the user
        category = UserCategory.query.filter(
            and_(
                UserCategory.owner == email,
                UserCategory.id == updated_transaction["categoryId"],
            )
        ).first()

        if not category:
            return create_response("Category not found", 404)

        # Retrieves the ID of the transaction to be updated
        recurring_transaction_id = updated_transaction["id"]

        # Fetches existing RecurringTransactions object
        recurring_transaction = RecurringTransactions.query.filter(
            RecurringTransactions.id == recurring_transaction_id
        ).first()

        if recurring_transaction is None:
            return create_response(f"Couldn't find recurring transaction with id of {recurring_transaction_id}", 404)

        # Updates fields of the recurring transaction with provided data
        update_recurring_transaction_fields(recurring_transaction, updated_transaction)
        db.session.commit()

        return create_response("Transaction updated successfully.", 200)
    except Exception as e:
        log(APP_NAME, "ERROR", f"Error updating recurring transaction for email: {email}, error: {str(e)}")
        return create_response("An error occurred while updating a recurring transaction", 500)


@transactions_bp.route("/create-recurring-transaction", methods=["POST"])
@jwt_required()
def create_recurring_transaction():
    """
    Create a new recurring transaction.
    """
    email = get_jwt_identity()

    try:
        new_transaction_data = request.get_json()

        # Validates the data against predefined rules
        validation_errors = validate_recurring_transaction(new_transaction_data)
        if validation_errors:
            return create_response("Object validation failed", 400, {"errors": validation_errors})

        # Query the Category based on the owner's email and the provided category name
        category = UserCategory.query.filter(
            and_(
                UserCategory.owner == email,
                UserCategory.id == new_transaction_data["categoryId"],
            )
        ).first()

        if not category:
            return create_response("Category not found", 404)

        transaction_amount = new_transaction_data["amount"]

        new_transaction_id = f"rt_{uuid.uuid4()}"

        # Creates a new Transaction object
        new_transaction = Transaction(
            id=new_transaction_id,
            arn="",
            userEmail=email,
            categoryId=category.categoryId,
            transactionAmount=transaction_amount,
            isRecurring=True,
        )
        db.session.add(new_transaction)

        # Creates a new RecurringTransactions object
        new_recurring_transaction = RecurringTransactions(
            userEmail=email, transactionId=new_transaction.id, scannedAt=None, transaction=new_transaction
        )

        # Updates fields of the recurring transaction with provided data
        update_recurring_transaction_fields(new_recurring_transaction, new_transaction_data)

        db.session.add(new_recurring_transaction)
        db.session.commit()

        return create_response("Transaction created successfully.", 200)
    except Exception as e:
        log(APP_NAME, "ERROR", f"Error creating new recurring transaction for email: {email}, error: {str(e)}")
        return create_response("An error occurred while creating a new recurring transaction", 500)


# Define the route for forcing a fetch of transactions
@transactions_bp.route("/force_fetch", methods=["POST"])
@jwt_required()
def force_fetch_transactions():
    """
    Force a fetch of transactions for a user.
    """
    # TODO: Implement logic to force fetching transactions
    pass


@transactions_bp.route("/get-monthly-spending-history", methods=["GET"])
@jwt_required()
def get_monthly_spending_history():
    """Get recieve history of monthly spending"""
    email = get_jwt_identity()

    try:
        spending_data = {}
        spending_history = UserCategorySpending.query.filter_by(
            userEmail=email,
        ).order_by(
            UserCategorySpending.date,
        )

        for monthly_category_spending in spending_history:
            date = monthly_category_spending.date
            spending_amount = monthly_category_spending.spendingAmount

            spending_data.setdefault(date, 0)
            spending_data[date] += spending_amount

        return create_response("Successfully fetched monthly spending history", 200, spending_data)
    except Exception as e:
        log(APP_NAME, "ERROR", f"Error fetching monthly spending history for email: {email}, error: {e}")
        return create_response("An error occurred while fetching monthly spending history", 500)
