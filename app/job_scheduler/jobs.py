import datetime
from app.database.models import CategoryMonthlyAveragesHistory, Transaction, User, db
from app.helper import fetch_users_for_scraping, process_recurring_transactions, transform_transactions_for_user
from app.logger import log
from app.merchant_aggregator import set_categories_for_transactions
from app.transactions_fetcher import fetch_transactions
from config.app import REGULAR_TRANSACTIONS_SCAN_DEPTH_IN_DAYS

def transactions_scanner(scheduler):
    APP_NAME = "Job - Transactions Scanner"

    # Define the range of dates for which transactions will be fetched
    end_date = datetime.datetime.now()
    start_date = end_date - datetime.timedelta(days=REGULAR_TRANSACTIONS_SCAN_DEPTH_IN_DAYS)

    with scheduler.flask_app.app_context():
        existing_transactions_dict = {}
        all_transactions_to_add_dict = {}
        all_transactions_to_add_list = []
        
        # Fetch users eligible for scraping
        users = fetch_users_for_scraping()

        # Iterate through each user and fetch their transactions
        for user in users:
            fetched_transactions = fetch_transactions(
                user_credentials={
                    "username": user.appUserCredentials.username,
                    "password": user.appUserCredentials.password,
                    "id": user.appUserCredentials.identityDocumentNumber,
                },
                start_date=start_date,
                end_date=end_date,
            )

            # Log and skip if no transactions are fetched for the user
            if not fetched_transactions:
                log(APP_NAME, "ERROR", f"Skipping transactions fetch for user: {user.email} due to an error")
                continue

            # Retrieve all existing transactions for the user
            all_user_transactions = Transaction.query.filter(Transaction.userEmail == user.email).all()
            all_user_transactions_dict = {transaction.arn: transaction for transaction in all_user_transactions}

            # Transform and process new and recurring transactions for the user
            new_transactions = transform_transactions_for_user(user, fetched_transactions)
            recurring_trans = [transaction for transaction in all_user_transactions if transaction.isRecurring]
            recurring_trans_to_add = process_recurring_transactions(recurring_trans)

            # Add all new and relevant recurring transactions to the list of transactions to be added
            all_transactions_to_add_list = all_transactions_to_add_list + new_transactions + recurring_trans_to_add
            all_transactions_to_add_dict = dict(all_transactions_to_add_dict, **{user.email: all_transactions_to_add_list})

            # Update the dictionary of all transactions with the new transactions
            existing_transactions_dict = dict(existing_transactions_dict, **all_user_transactions_dict)

        unparsed_transactions_dict = {}
        # Iterate through the transactions to be added and log their details
        for email, transaction_list in all_transactions_to_add_dict.items():

            for transaction in transaction_list:
                # Check if the transaction already exists in the existing_transactions_dict
                if transaction.arn not in existing_transactions_dict:
                    if email in unparsed_transactions_dict:
                        unparsed_transactions_dict[email].append(transaction)
                    else:
                        unparsed_transactions_dict[email] = [transaction]
        
        # Set categories for all unparsed transactions
        parsed_transactions_dict = set_categories_for_transactions(unparsed_transactions_dict)
        for parsed_transaction in parsed_transactions_dict.values():
            db.session.add_all(parsed_transaction)
        
        db.session.commit()
   
    # Log the completion of the transactions scanner job
    log(APP_NAME, "INFO", "Finished running transactions scanner")


def calculate_monthly_averages(scheduler):
    APP_NAME = "Job - Monthly Averages Calculator"
    log(APP_NAME, "INFO", "Running monthly averages calculator")

    with scheduler.flask_app.app_context():
        # Get all users
        users = User.query.all()

        # Get all CategoryMonthlyAveragesHistory rows 
        averages = CategoryMonthlyAveragesHistory.query.all()

        # Iterate over averages 
        #TODO: Implement -> calculate monthly averages for each category





    log(APP_NAME, "INFO", "Finished running monthly averages calculator")
    # db.session.commit()