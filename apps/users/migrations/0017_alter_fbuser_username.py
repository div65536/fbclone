# Generated by Django 4.2.20 on 2025-04-28 06:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0016_alter_fbuser_username"),
    ]

    operations = [
        migrations.AlterField(
            model_name="fbuser",
            name="username",
            field=models.CharField(max_length=254, unique=True),
        ),
    ]
