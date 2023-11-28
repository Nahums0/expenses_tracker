from app.job_scheduler.jobs.transactions_categorizer import categorize_all_transactions
from app.job_scheduler.jobs.transactions_scanner import scan_users_transactions
from app.job_scheduler.jobs.monthly_spending_aggregator import aggregate_monthly_spending

scheduled_jobs_dict = {
    "transactions_scanner": {
        "id":"transactions_scanner",
        "name": "Transactions Scanner",
        "func": scan_users_transactions,
        "schedule_args": {"trigger": "interval", "minutes": 3},
        "immediate_run": False,
    },
    "transactions_categorizer": {
        "id":"transactions_categorizer",
        "name": "Transactions Categorizer",
        "func": categorize_all_transactions,
        "schedule_args": {"trigger": "interval", "minutes": 5},
        "immediate_run": False,
    },
    "monthly_spending_calculator": {
        "id":"monthly_spending_calculator",
        "name": "Monthly Spending Calculator",
        "func": aggregate_monthly_spending,
        "schedule_args": {"trigger": "interval", "minutes": 5},
        "immediate_run": False,
        "args": {
            "users_list": None,
            "deep_scan": True,
        },
    },
}
