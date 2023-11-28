import datetime
from app.database.models import Transaction, User, db
from app.helper import add_failed_login_user_warning, fetch_users_for_scraping
from app.logger import log
from app.credit_card_adapters.max_fetcher import fetch_transactions_from_max
from app.job_scheduler.jobs.monthly_spending_aggregator import aggregate_monthly_spending
from app.job_scheduler.jobs.transactions_categorizer import categorize_all_transactions
from config.app import DEEP_TRANSACTIONS_SCAN_DEPTH_IN_DAYS, SHALLOW_TRANSACTION_SCAN_DEPTH_IN_DAYS

APP_NAME = "Transactions Scanner"


def _fetch_user_transactions(user, dates):
    """Fetch transactions for a user within a given date range."""

    try:
        log(APP_NAME, "DEBUG", f"Fetching transactions for user {user.email}, monthView: {dates == None}")
        transactions = fetch_transactions_from_max(
            user_credentials={
                "username": user.appUserCredentials.username,
                "password": user.appUserCredentials.password,
                "id": user.appUserCredentials.identityDocumentNumber,
            },
            user_email=user.email,
            dates=dates,
        )
        log(
            APP_NAME,
            "DEBUG",
            f"Successfully fetched transactions for user {user.email}, received {len(transactions)} transactions",
        )
        return transactions
    except Exception as e:
        log(APP_NAME, "ERROR", f"Failed to fetch transactions for user {user.email}. Error: {e}")
        return None


def _get_existing_user_transactions(user_email):
    """Retrieve existing transactions for a user from the database."""

    transactions = Transaction.query.filter(Transaction.userEmail == user_email).all()
    confirmed = []
    pending = []

    for t in transactions:
        if t.isPending:
            pending.append(t)
        else:
            confirmed.append(t)

    return confirmed, pending


def _calculate_scan_depth(user):
    """Calculate the depth of transactions scan for a user."""

    last_scan_date = user.lastTransactionsScanDate
    if last_scan_date:
        return None
    else:
        start_date = datetime.datetime.now() - datetime.timedelta(days=DEEP_TRANSACTIONS_SCAN_DEPTH_IN_DAYS)
        end_date = datetime.datetime.now()
        return start_date, end_date


def scan_users_transactions(scheduler, users_list=None):
    """Fetch and process transactions"""

    log(APP_NAME, "INFO", "Starting transactions scanner")
    try:
        with scheduler.flask_app.app_context():
            if isinstance(users_list, list):
                users_to_scan = User.query.filter(User.email.in_(users_list)).all()
                log(APP_NAME, "DEBUG", f"Perfoming a focused transactions scan on {len(users_list)} users")
            else:
                # Fetch users to scan and those to skip
                users_to_scan, skipped_users = fetch_users_for_scraping()

                # Log scan type and users count
                if len(users_to_scan) < 0:
                    log(APP_NAME, "DEBUG", f"Perfoming a transactions scan on {len(users_list)} users")

                    if len(skipped_users) > 0:
                        log(APP_NAME, "DEBUG", f"The following users were omitted from the scan: {', '.join(skipped_users)}")
                else:
                    # Exit if no users to scan
                    log(APP_NAME, "INFO", "No users to scan")
                    return

            transactions_to_add = {}
            for user in users_to_scan:
                scan_dates = _calculate_scan_depth(user)

                # Fetch transactions for the user within the scan dates
                user_transactions = _fetch_user_transactions(user=user, dates=scan_dates)

                # Add user warnings for failed scans
                if user_transactions is None:
                    add_failed_login_user_warning(user.email)
                else:
                    transactions_to_add[user.email] = user_transactions

            # Count new transactions for logging purposes
            transactions_count = 0
            for transactions in transactions_to_add.values():
                transactions_count += len(transactions)

            log(APP_NAME, "INFO", f"Transaction scanner fetched {transactions_count} transactions")

            if transactions_count > 0:
                new_transactions = {}

                # Compare fetched transactions with existing ones to find new transactions
                for email, transactions in transactions_to_add.items():
                    if email not in new_transactions:
                        new_transactions[email] = []

                    # Get existing confirmed and pending transactions for the user
                    confirmed_user_transactions, pending_user_transactions = _get_existing_user_transactions(email)

                    # Insert to a dict for a faster lookout
                    confirmed_user_transactions_dict = {
                        transaction.id: transaction for transaction in confirmed_user_transactions
                    }
                    pending_user_transactions_dict = {
                        transaction.uid: transaction for transaction in pending_user_transactions
                    }

                    # Check each transaction to see if it's new or already exists
                    for transaction in transactions:
                        is_pending_update = (
                            transaction.uid in pending_user_transactions_dict and transaction.isPending is False
                        )
                        is_confirmed_new = (
                            transaction.id not in confirmed_user_transactions_dict
                            and transaction.uid not in pending_user_transactions_dict
                        )

                        if is_pending_update:
                            # delete the old pending transaction from the database.
                            to_delete = pending_user_transactions_dict[transaction.uid]
                            db.session.delete(to_delete)
                        if is_pending_update or is_confirmed_new:
                            # If the transaction is either a new transaction or an update to a pending transaction,
                            # add it to the list of new transactions for this user.
                            new_transactions[email].append(transaction)

                # Add new transactions to the database
                try:
                    for transactions in new_transactions.values():
                        db.session.add_all(transactions)

                    # Update the last transaction scan date for each user
                    for user in users_to_scan:
                        user.lastTransactionsScanDate = datetime.datetime.now()

                    db.session.commit()
                except Exception as e:
                    log(APP_NAME, "ERROR", f"Failed to set categorized transactions. Error: {str(e)}")
                    return
            log(APP_NAME, "INFO", "Finished transactions scan")

    except Exception as e:
        log(APP_NAME, "ERROR", f"An error occured while scanning transactions: {e}")
        raise e
