from app.job_scheduler.jobs.monthly_averages_aggregator import calculate_monthly_averages
from app.job_scheduler.jobs.transactions_categorizer import categorize_all_transactions
from app.job_scheduler.jobs.transactions_scanner import scan_users_transactions
from app.job_scheduler.jobs.monthly_spending_aggregator import aggregate_monthly_spending

scheduled_jobs = [
    {
        "name": "Transactions Scanner",
        "func": scan_users_transactions,
        "schedule_args": {"trigger": "interval", "minutes": 30},
        "immediate_run": True,
    },
    {
        "name": "Monthly Averages Calculator",
        "func": calculate_monthly_averages,
        "schedule_args": {"trigger": "interval", "hours": 6},
        "immediate_run": False,
    },
    {
        "name": "Transactions Categorizer",
        "func": categorize_all_transactions,
        "schedule_args": {"trigger": "interval", "minutes": 5},
        "immediate_run": True,
    },
    {
        "name": "Monthly Spending Calculator",
        "func": aggregate_monthly_spending,
        "schedule_args": {"trigger": "interval", "minutes": 5},
        "immediate_run": True,
        "args": {
            "users_list": None,
            "deep_scan": True,
        },
    },
    # Optional non deep scan aggregate_monthly_spending configuration
    #
    # {
    #     "name": "Monthly Spending Calculator",
    #     "func": aggregate_monthly_spending,
    #     "schedule_args": {"trigger": "interval", "minutes": 2},
    #     "immediate_run": False,
    #     "args": {
    #         "users_list": None,
    #         "deep_scan": False,
    #     },
    # },
]
