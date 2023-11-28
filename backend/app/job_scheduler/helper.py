from app.logger import log

APP_NAME = "Job Scheduler"


def run_jobs(scheduler, job_list):
    """
    Runs a list of jobs. Each job is expected to have a 'func' attribute pointing to the function to run,
    and an 'args' attribute containing the arguments for the function.
    """
    count = 1
    for job in job_list:
        try:
            log(APP_NAME, "DEBUG", f"Triggering job {count}/{len(job_list)}")

            # Extract the function and arguments from the job
            job_func = job.get("func")
            job_args = job.get("args", {})

            job_func(scheduler, *job_args.values())
        except Exception as e:
            log(APP_NAME, "ERROR", f"Job {job.get('id', 'Unknown')} ({count}/{len(job_list)}) failed, error: {e}")
            break

        count += 1