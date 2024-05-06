from app.model import Job, Notification, Evaluation
from app.database import get_db
from datetime import datetime
# import time
from app.script import run_algorithm
import json
import numpy as np


class NumpyArrayEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


def run_calculations(job_id: str, user_id: str, tickers=[]):
    db = next(get_db())
    job = db.get(Job, job_id)
    job.startedAt = datetime.now()

    try:
        data = run_algorithm(tickers)

        evaluation = db.get(Evaluation, job.evaluation)
        # print(evaluation, evaluation.data)
        evaluation.data = json.dumps(data, cls=NumpyArrayEncoder)
        # print(job_id, data)

        job.completedAt = datetime.now()
        job.done = True
        db.add(job, evaluation)
        # evaluation.commit()
        db.commit()

        notification = Notification(
            user=user_id, message=f"{job.evaluation}", success=True)

        db.add(notification)
        db.commit()
        print("Done job ...................................................................................")
    except Exception as e:
        notification = Notification(
            user=user_id, message=f"{job.evaluation}", success=False)
        db.add(notification)
        db.commit()
        print(e)
        print("Error job ...................................................................................")

        #
        # print(f"running calculations for job.id:{job.done}")
