# Generated by Django 4.1.5 on 2023-01-05 11:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bulletin', '0005_alter_post_text'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='response',
            new_name='like',
        ),
    ]