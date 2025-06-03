from django.core.management.base import BaseCommand
from users.models import FbUser
from datetime import timedelta
from django.utils import timezone

class Command(BaseCommand):
    help = 'Deletes users who have been inactive for 15 days'

    def handle(self, *args, **options):
        inactive_users = FbUser.objects.filter(
            last_login__lt=timezone.now() - timedelta(days=15),
            is_active=True
        )
        print(inactive_users)
        for user in inactive_users:
            print(f"Deleted {user}")
            user.delete()
            