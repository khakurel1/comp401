# Import necessary modules and classes
from app.model import Job, Notification
from app.database import get_db
from datetime import datetime
import time

# Define the run_calculations function
def run_calculations(job_id: str, user_id: str):
    # Get a database connection from the pool
    db = next(get_db())

    # Retrieve the job with the specified job_id from the database
    job = db.get(Job, job_id)

    # Update the startedAt attribute of the job with the current date and time
    job.startedAt = datetime.now()

    # Simulate the time it takes to perform calculations for the job by pausing the program for 20 seconds
    time.sleep(20)

    # Update the completedAt attribute of the job with the current date and time
    job.completedAt = datetime.now()

    # Set the done attribute of the job to True to indicate that the job has been completed
    job.done = True

    # Add the updated job object to the database
    db.add(job)

    # Commit the changes to the database
    db.commit()

    # Create a notification object with the user_id and a message indicating that the job has been completed
    notification = Notification(
        user=user_id,
        message=f"Job completed id:{job_id}"
    )

    # Add the notification object to the database
    db.add(notification)

    # Commit the changes to the database
    db.commit()

    # print(f"running calculations for job.id:{job.done}")
