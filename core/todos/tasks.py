from core import celery
from core.utils import send_email


@celery.task
def send_creation_mail(user_email):
    send_email(user_email, "Testing", "Test.")
    return f"Mail sent to {user_email}"
