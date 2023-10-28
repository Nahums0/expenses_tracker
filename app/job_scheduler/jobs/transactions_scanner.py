import datetime
from app.database.models import Transaction, db
from app.helper import add_failed_login_user_warning, fetch_users_for_scraping, process_recurring_transactions, transform_transactions_for_user
from app.logger import log
from app.transaction_fetchers.max_fetcher import fetch_transactions_from_max
from config.app import DEEP_TRANSACTIONS_SCAN_DEPTH_IN_DAYS

APP_NAME = "Transactions Scanner"

def _fetch_user_transactions(user, start_date, end_date):
    """Fetch transactions for a user within a given date range."""

    try:
        log(APP_NAME, "DEBUG", f"Fetching transactions for user {user.email}. start_date: {start_date.date()}, end_date: {end_date.date()}")
        transactions = fetch_transactions_from_max(
            user_credentials={
                "username": user.appUserCredentials.username,
                "password": user.appUserCredentials.password,
                "id": user.appUserCredentials.identityDocumentNumber
            },
            user_email=user.email,
            start_date=start_date,
            end_date=end_date,
        )
        log(APP_NAME, "DEBUG", f"Successfully fetched transactions for user {user.email}, received {len(transactions)} transactions")
        return transactions
    except Exception as e:
        log(APP_NAME, "ERROR", f"Failed to fetch transactions for user {user.email}. Error: {str(e)}")
        return None


def _get_existing_user_transactions(user_email):
    """Retrieve existing transactions for a user from the database."""

    return Transaction.query.filter(Transaction.userEmail == user_email).all()


def _calculate_scan_depth(user):
    """Calculate the depth of transactions scan for a user."""

    last_scan_date = user.lastTransactionsScanDate
    return DEEP_TRANSACTIONS_SCAN_DEPTH_IN_DAYS if last_scan_date is None else (datetime.datetime.now() - last_scan_date).days + 1


def scan_users_transactions(scheduler):
    """Scan and process transactions for all users."""

    log(APP_NAME, "INFO", "Starting transactions scanner")
    try:
        with scheduler.flask_app.app_context():
            users_to_scan, skipped_users = fetch_users_for_scraping()
            if len(skipped_users) > 0:
                log(APP_NAME, "DEBUG", f"The following users were omitted from the scan: {', '.join(skipped_users)}")

            if len(users_to_scan) < 0:
                log(APP_NAME, "INFO", "No users to scan")
                return

            transactions_to_add = {}
            for user in users_to_scan:
                scan_depth = _calculate_scan_depth(user)
                user_transactions = _fetch_user_transactions(user, datetime.datetime.now() - datetime.timedelta(days=scan_depth), datetime.datetime.now())
                if user_transactions is None:
                    add_failed_login_user_warning(user.email)
                else:
                    transactions_to_add[user.email] = user_transactions

            transactions_count = 0
            for transactions in transactions_to_add.values():
                transactions_count += len(transactions)

            log(APP_NAME, "INFO", f"Transaction scanner found {transactions_count} new transactions")

            if transactions_count > 0:
                new_transactions = {}

                for email, transactions in transactions_to_add.items():
                    existing_user_transactions = _get_existing_user_transactions(email)
                    existing_user_transactions = {transaction.id: transaction for transaction in existing_user_transactions}

                    new_user_transactions = [transaction for transaction in transactions if f"{email}_{transaction.arn}" not in existing_user_transactions]
                    new_transactions[email] = new_user_transactions

                try:
                    for transactions in new_transactions.values():
                        db.session.add_all(transactions)
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