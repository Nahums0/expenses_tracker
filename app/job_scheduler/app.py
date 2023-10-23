from apscheduler.schedulers.background import BackgroundScheduler
from app.logger import log
from lib.singleton.singleton import Singleton
from app.job_scheduler.jobs_config import scheduled_jobs
import datetime

APP_NAME = "Job Scheduler"

@Singleton
class BackgroundSchedulerSingleton:
    """
    A Singleton class of the apscheduler.schedulers.background.BackgroundScheduler class
    """
    
    def __init__(self, app) -> None:
        # Initialize the background scheduler
        self.scheduler = BackgroundScheduler()
        
        # Store the Flask app instance for potential future use
        self.flask_app = app

        # Schedule jobs based on the provided configuration
        for job in scheduled_jobs:
            scheduled_job = self.scheduler.add_job(job['func'], args=(self,), **job['schedule_args'])
            
            # If the job is marked for immediate run, set its next run time to now
            if job['immediate_run']:
                scheduled_job.modify(next_run_time=datetime.datetime.now())
                log(APP_NAME, "DEBUG", f"Running job: {job['name']} - 'immediate_run' is True")

            # Log a message indicating that the job has been scheduled
            log(APP_NAME, "DEBUG", f"Scheduled job: {job['name']}")

def start_scheduler(app):
    """
    Initiate and start the background scheduler.
    """
    
    # Get the scheduler instance and start it
    scheduler = BackgroundSchedulerSingleton.get_instance(app=app).scheduler
    scheduler.start()
