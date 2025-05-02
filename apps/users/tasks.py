from django.core.mail import send_mail
from fbclone.settings.base import EMAIL_HOST_USER
from celery import shared_task

@shared_task
def send_registration_email(email_address, message):
    send_mail(
        "Registration Succesfull",
        f"\t{message}\n\nThank you!",
        EMAIL_HOST_USER,
        [email_address],
        fail_silently=False
    )