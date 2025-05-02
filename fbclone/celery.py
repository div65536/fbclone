import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fbclone.settings.base")
app = Celery("fbclone")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()