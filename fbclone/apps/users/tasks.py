from django.core.mail import send_mail
from fbclone.settings.base import EMAIL_HOST_USER
from celery import shared_task
from users.models import FbUser
from datetime import date

@shared_task
def send_registration_email(email_address, message):
    send_mail(
        "Registration Succesfull",
        f"\t{message}\n\nThank you!",
        EMAIL_HOST_USER,
        [email_address],
        fail_silently=False
    )

@shared_task
def happy_birthday():
    today = date.today()
    users = FbUser.objects.all()
    for user in users:
        if today == user.date_of_birth:
            print(user.first_name)
            send_mail("Happy Birthday",f"\tDear{user.first_name}\n\n Happy Birthday", EMAIL_HOST_USER,[user.email],fail_silently=True)
