# Generated by Django 4.2.20 on 2025-04-21 09:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0012_fbuser_username_alter_fbuser_email"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="fbuser",
            name="username",
        ),
    ]
