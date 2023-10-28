from collections import defaultdict
from app.database.models import CategoryMonthlyAveragesHistory, Transaction, User, db
from app.logger import log
from app.merchant_aggregator.merchant_aggregator import categorize_for_all_users
from sqlalchemy import case

APP_NAME = "Transactions Categorizer"

def categorize_all_transactions(scheduler):
    """Categorizes all transactions that have not been categorized yet."""

    log(APP_NAME, "INFO", "Transactions Categorizer started")
    try:
        with scheduler.flask_app.app_context():
            # Query the database
            unparsed_transactions = Transaction.query.filter(Transaction.categoryId == -1).all()
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
            log(APP_NAME, "INFO", f"Categorizing transactions for {len(unparsed_transactions_dict)} unqiue users, total transactions: {len(unparsed_transactions)}")
            updated_transactions, user_parsed_categories = categorize_for_all_users(unparsed_transactions_dict)

            # Update db with new category values
            db.session.bulk_update_mappings(Transaction, updated_transactions)

            # Filter duplicate values
            user_parsed_categories = {
                user_parsed_category.chargingBusiness: user_parsed_category
                for user_parsed_category in user_parsed_categories
            }.values()
            db.session.add_all(user_parsed_categories)

            db.session.commit()
            log(APP_NAME, "INFO", "Transactions Categorizer finished")
    except Exception as e:
        log(APP_NAME, "ERROR", f"An error occured while categorizing transactions: {e}")
        raise e