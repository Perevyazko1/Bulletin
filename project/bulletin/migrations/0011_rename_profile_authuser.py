# Generated by Django 4.1.5 on 2023-01-07 20:03

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bulletin', '0010_profile_authenticate'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Profile',
            new_name='AuthUser',
        ),
    ]