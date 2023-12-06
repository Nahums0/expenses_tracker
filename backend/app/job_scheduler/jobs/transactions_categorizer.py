from sqlalchemy import or_
from app.database.models import Transaction, db
from app.logger import log
from app.merchant_aggregator.merchant_aggregator import categorize_for_all_users

APP_NAME = "Transactions Categorizer"


def categorize_all_transactions(scheduler, users_list=None):
    """Categorizes all transactions that have not been categorized yet."""

    log_message = "Transactions Categorizer started"
    if isinstance(users_list, list):
        log_message += f", perfoming a focused scan for {len(users_list)}"
    else:
        log_message += f", perfoming a scan for all users"
    log(APP_NAME, "INFO", log_message)

    try:
        with scheduler.flask_app.app_context():
            unparsed_transactions = fetch_transaction(users_list)
            unparsed_transactions_dict = {}

            if len(unparsed_transactions) == 0:
                log(APP_NAME, "INFO", "Transactions Categorizer didn't find unparsed transactions")
                return

            # Create a dictionary of unparsed transactions by user email
            for transaction in unparsed_transactions:
                if transaction.userEmail not in unparsed_transactions_dict:
                    unparsed_transactions_dict[transaction.userEmail] = []
                unparsed_transactions_dict[transaction.userEmail].append(transaction)

            # Categorize unparsed transactions
            log(
                APP_NAME,
                "INFO",
                f"Categorizing transactions for {len(unparsed_transactions_dict)} unqiue users, total transactions: {len(unparsed_transactions)}",
            )
            categorize_for_all_users(unparsed_transactions_dict)
            log(APP_NAME, "INFO", "Transactions Categorizer finished")
    except Exception as e:
        log(APP_NAME, "ERROR", f"An error occured while categorizing transactions: {e}")
        raise e


def fetch_transaction(users_list):
    query = Transaction.query.filter(
        or_(
            Transaction.categoryId == -1,
            Transaction.categoryId == None,
        )
    )

    if isinstance(users_list, list):
        query = query.filter(Transaction.userEmail.in_(users_list))

    unparsed_transactions = query.order_by(Transaction.purchaseDate.desc()).all()
    return unparsed_transactions
