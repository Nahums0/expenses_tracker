from app.logger import log
from app.database.models import Transaction, User, UserCategorySpending, db
from datetime import datetime
from app.helper import date_to_number

APP_NAME = "Monthly Spending Aggregator"


def aggregate_monthly_spending(scheduler, users_list=None, deep_scan=False):
    """Aggregates all users' monthly spending."""

    log(APP_NAME, "INFO", f"Starting {APP_NAME}, deep_scan: {deep_scan}, users: {users_list}")

    with scheduler.flask_app.app_context():
        try:
            # Select users based on the given list or all users if none is provided.
            if isinstance(users_list, list):
                users = User.query.filter(User.email.in_(users_list)).all()
                log(APP_NAME, "DEBUG", f"Perfoming a focused monthly spending aggregation on {len(users_list)} users")
            else:
                users = User.query.all()
                log(APP_NAME, "DEBUG", "Perfoming am all users monthly spending aggregation")

            for user in users:
                # If a deep scan is performed, all of the previous UserCategorySpending data can be delete
                if deep_scan:
                    UserCategorySpending.query.filter(UserCategorySpending.userEmail == user.email).delete(
                        synchronize_session=False
                    )

                # Fetch user transactions and calculate spending data.
                transactions = get_transactions_from_db(user, deep_scan)
                spending_data = get_monthly_spending_data(transactions)

                # Process spending data for each user and modify database.
                for spending_date, categories in spending_data.items():
                    for categoryId, spending_amount in categories.items():
                        monthly_spending_object = UserCategorySpending.query.filter(
                            UserCategorySpending.userEmail == user.email,
                            UserCategorySpending.date == spending_date,
                            UserCategorySpending.userCategoryId == categoryId,
                        ).first()

                        # Either add new UserCategorySpending row or update existing one
                        if not monthly_spending_object:
                            monthly_spending_object = UserCategorySpending(
                                userEmail=user.email,
                                date=spending_date,
                                userCategoryId=categoryId,
                                spendingAmount=spending_amount,
                            )
                            db.session.add(monthly_spending_object)
                        else:
                            monthly_spending_object.spendingAmount = spending_amount
                user.initialSetupDone = True

            db.session.commit()
            log(APP_NAME, "INFO", f"{APP_NAME} finished")
        except Exception as e:
            db.session.rollback()
            log(APP_NAME, "ERROR", f"Error in monthly spending aggregation: {e}")
            raise e


def get_transactions_from_db(user, full_history):
    query = Transaction.query.filter(Transaction.userEmail == user.email, Transaction.isRecurring == False)

    # Limit to current month's transactions if not full history.
    if not full_history:
        current_date = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        query = query.filter(Transaction.purchaseDate >= current_date)

    return query.order_by(Transaction.purchaseDate)


def get_monthly_spending_data(transactions):
    # Aggregate spending data from transactions.

    spending_data = {}
    for transaction in transactions:
        transaction_date = date_to_number(transaction.purchaseDate)
        spending_data.setdefault(transaction_date, {}).setdefault(transaction.categoryId, 0)
        spending_data[transaction_date][transaction.categoryId] += transaction.transactionAmount

    return spending_data
