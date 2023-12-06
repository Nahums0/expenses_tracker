def trigger_transactions_processing_jobs(users, deep_scan):
    """Initiates a processing pipeline by triggering a series of backend jobs"""

    from app.job_scheduler.jobs_config import scheduled_jobs_dict
    from app.job_scheduler.app import SchedulerInstance

    chained_jobs = [
        scheduled_jobs_dict["transactions_categorizer"],
        scheduled_jobs_dict["monthly_spending_calculator"],
    ]

    custom_args = {
        "transactions_categorizer": {"args": {"users_list": users}},
        "monthly_spending_calculator": {"args": {"users_list": users, "deep_scan": deep_scan}},
    }
    scheduler = SchedulerInstance.get_instance()
    scheduler.trigger_jobs(chained_jobs, custom_args)
