# Generated by Django 4.2.20 on 2025-04-09 05:47

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("posts", "0004_likes_created_at"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Likes",
            new_name="Like",
        ),
    ]
