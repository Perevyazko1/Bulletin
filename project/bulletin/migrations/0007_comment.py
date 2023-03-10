# Generated by Django 4.1.5 on 2023-01-05 13:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bulletin', '0006_rename_response_post_like'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='Отклик')),
                ('dateCreation', models.DateTimeField(auto_now_add=True, verbose_name='Дата')),
                ('commentPost', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bulletin.post', verbose_name='Объявление')),
                ('commentUser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Комментарий к новости',
                'verbose_name_plural': 'Комментарии к новостям',
            },
        ),
    ]
