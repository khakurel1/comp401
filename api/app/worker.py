from app.model import Job, Notification
from app.database import get_db
from datetime import datetime
# import time
from app.script import run_algorithm


def run_calculations(job_id: str, user_id: str, tickers=[]):
    db = next(get_db())
    job = db.get(Job, job_id)
    job.startedAt = datetime.now()

    run_algorithm(tickers)

    job.completedAt = datetime.now()
    job.done = True
    db.add(job)
    db.commit()

    notification = Notification(
        user=user_id, message=f"Job completed id:{job_id}")
    db.add(notification)
    db.commit()
    #
    # print(f"running calculations for job.id:{job.done}")
