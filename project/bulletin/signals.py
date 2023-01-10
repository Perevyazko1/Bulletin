from django.conf import settings
from django.contrib.auth.models import User
from django.core.cache import cache
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import AuthUser, Post, Response
from .tasks import send_email


@receiver(post_save, sender=Response)
def update_status_response(instance, **kwargs):
    if not instance.status:
        id = instance.id
        r = Response.objects.get(id=id)
        user = r.commentUser.username
        email = [r.commentUser.email]
        post = r.commentPost.get_absolute_url()
        message = 'На твой отклик ответили.'
        send_email.delay(user, email, post, message)


@receiver(post_save, sender=Response)
def get_response(created, instance, **kwargs):
    if created:
        id = instance.id
        r = Response.objects.get(id=id)
        user = r.commentPost.author.username
        email = [r.commentPost.author.email]
        post = r.commentPost.get_absolute_url()
        message = 'Вам оставили отклик.'
        send_email.delay(user, email, post, message)


@receiver(post_save, sender=User)
def send_response(created, instance, **kwargs):
    if created:
        p = AuthUser.objects.create(user=instance)

        email = [instance.email]
        msg = EmailMultiAlternatives(
            subject='Код авторизации',
            body=f'Код авторизации {p.uuid}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=email,
        )
        msg.send()


@receiver(post_save, sender=Post)
def update_post(sender, instance, **kwargs):
    id = str(instance.id)
    cache.delete(f'bulletins-{id}')