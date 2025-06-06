from django.core.management.base import BaseCommand
from users.models import FbUser
from datetime import timedelta
from django.utils import timezone

class Command(BaseCommand):
    help = 'list email of users'

    def handle(self, *args, **options):
        users = FbUser.objects.all()
        for user in users:
            print(user.email)