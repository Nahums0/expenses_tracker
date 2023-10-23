from app.job_scheduler.jobs import transactions_scanner, calculate_monthly_averages

scheduled_jobs = [
    {
        "name": "Transactions Scanner",
        "func": transactions_scanner,
        "schedule_args": {"trigger": "interval", "seconds": 30},
        "immediate_run": True,
    },
    {
        "name": "Monthly Averages Calculator",
        "func": calculate_monthly_averages,
        "schedule_args": {"trigger": "interval", "hours": 6},
        "immediate_run": True,
    }
]