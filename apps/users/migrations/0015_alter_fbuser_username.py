# Generated by Django 4.2.20 on 2025-04-21 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0014_fbuser_username"),
    ]

    operations = [
        migrations.AlterField(
            model_name="fbuser",
            name="username",
            field=models.CharField(max_length=254, unique=True),
        ),
    ]
