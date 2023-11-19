from apscheduler.schedulers.background import BackgroundScheduler
from app.logger import log
from lib.singleton.singleton import Singleton
from app.job_scheduler.jobs_config import scheduled_jobs
import datetime

APP_NAME = "Job Scheduler"

@Singleton
class SchedulerInstance:
    """Singleton wrapper around the BackgroundScheduler."""

    def __init__(self, app) -> None:
        # Initialize the background scheduler and Flask app
        self.scheduler = BackgroundScheduler()
        self.flask_app = app
        
        # Schedule the configured jobs
        self._schedule_jobs()

    def _schedule_jobs(self):
        """Schedule jobs based on the provided configuration."""
        
        for job_config in scheduled_jobs:
            # Extract job specific arguments
            job_args = job_config.get("args", {})

            # Add each job to the scheduler
            job = self.scheduler.add_job(job_config['func'], args=(self, *job_args.values()), **job_config['schedule_args'])
            
            # If immediate_run is set, modify the job's next run time
            if job_config['immediate_run']:
                job.modify(next_run_time=datetime.datetime.now())
                log(APP_NAME, "DEBUG", f"Immediately running job: {job_config['name']}")
            
            # Log job scheduling completion
            log(APP_NAME, "DEBUG", f"Job scheduled successfully: {job_config['name']}")


def start_scheduler(app):
    """Initiate and start the background scheduler."""
    
    # Log the initiation of the scheduler
    log(APP_NAME, "INFO", "Starting job scheduler")
    
    # Get the singleton instance of the scheduler and start it
    scheduler_instance = SchedulerInstance.get_instance(app=app)
    scheduler_instance.scheduler.start()
    
    # Log the completion of the scheduler start process
    log(APP_NAME, "INFO", "Job scheduler initiated")
