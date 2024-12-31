from celery import Celery
import os
from dotenv import load_dotenv

load_dotenv()

celery_app = Celery(
    "api_integrations",
    broker=os.getenv("CELERY_BROKER_URL"),
    backend=os.getenv("CELERY_RESULT_BACKEND"),
    include=["async_tasks.tasks"]
)

# Configuration
celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    enable_utc=True,
    worker_prefetch_multiplier=4,
    task_routes={
        "scraping_tasks.*": {"queue": "scraping"},
        "analysis_tasks.*": {"queue": "analysis"},
        "database_tasks.*": {"queue": "database"}
    },
    task_default_queue="default",
    task_acks_late=True,
    task_reject_on_worker_lost=True,
    task_track_started=True,
    worker_max_tasks_per_child=100,
    broker_connection_retry_on_startup=True
)

if __name__ == "__main__":
    celery_app.start()
