from app.job_scheduler.jobs.monthly_averages_aggregator import monthly_averages_calculator
from app.job_scheduler.jobs.transactions_categorizer import categorize_all_transactions
from app.job_scheduler.jobs.transactions_scanner import scan_users_transactions

scheduled_jobs = [
    {
        "name": "Transactions Scanner",
        "func": scan_users_transactions,
        "schedule_args": {"trigger": "interval", "seconds": 30},
        "immediate_run": True,
    },
    {
        "name": "Monthly Averages Calculator",
        "func": monthly_averages_calculator,
        "schedule_args": {"trigger": "interval", "hours": 6},
        "immediate_run": False,
    },
    {
        "name": "Transactions Categorizer",
        "func": categorize_all_transactions,
        "schedule_args": {"trigger": "interval", "minutes": 1},
        "immediate_run": True,
    }
]