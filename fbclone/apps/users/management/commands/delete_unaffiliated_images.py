from django.core.management.base import BaseCommand
from users.models import FbUser
from datetime import timedelta
from django.utils import timezone
from django.conf import settings
import os

class Command(BaseCommand):
    help = 'Deletes users who have been inactive for 15 days'

    def handle(self, *args, **options):
        users = FbUser.objects.all()
        posts = FbUser.objects.all()

        for user in users:
            print(user.profile_picture)
