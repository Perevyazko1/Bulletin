from django.conf import settings
from django.contrib.auth.models import Group, User
from django.core.cache import cache
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed, post_delete, post_save, pre_delete, pre_init, post_init, pre_save
from django.dispatch import receiver
from django.template.loader import render_to_string

from .models import Response, Post, AuthUser
from django.core.mail import send_mail


# from .tasks import send_notifications


# @receiver(m2m_changed, sender=PostCategory)
# def notify_about_new_post(sender, instance, **kwargs):
#     if kwargs['action'] == 'post_add':
#         categories = instance.category.all()
#         subscribes: list[str] = []
#         # users: list[str] = []
#         for category in categories:
#             subscribes += category.subscribes.all()
#         # users = [s.username for s in subscribes]
#         # subscribes = [s.email for s in subscribes]
#         # print(users)
#         # print(subscribes)
#         send_notifications.delay(instance.id, instance.title, instance.text)


# def send_new_user(user, email):
#     html_content = render_to_string(
#         'new_user.html',
#         {
#             'link': f'{settings.SITE_URL}/news/profile/',
#             'user': user,
#         }
#     )
#     message = EmailMultiAlternatives(
#         subject='Регистрация',
#         body='',  # это то же, что и message
#         from_email=settings.DEFAULT_FROM_EMAIL,
#         to=email,  # это то же, что и recipients_list
#
#     )
#     message.attach_alternative(html_content, 'text/html')  # добавляем html
#     message.send()  # отсылаем
#
#
# @receiver(post_save, sender=User)
# def hello_new_user(sender, instance, created, **kwargs):
#     if created:
#         email = [instance.email]
#         user = instance
#         send_new_user(user, email)
#         group = Group.objects.get(id=2)
#         user.groups.add(group)

def send_email(user, email, post, message, subject):
    html_content = render_to_string(
        'send_response.html',
        {
            'link': settings.SITE_URL,
            'post': post,
            'user': user,
            'message':message
        }
    )

    msg = EmailMultiAlternatives(
        subject=message,
        body='',  # это то же, что и message
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=email,  # это то же, что и recipients_list
    )
    msg.attach_alternative(html_content, 'text/html')  # добавляем html
    msg.send()  # отсылаем


@receiver(pre_save, sender=Response)
def update_status_response(instance, **kwargs):
    if instance.status:
        id = instance.id
        r = Response.objects.get(id=id)
        user = r.commentUser.username
        email = [r.commentUser.email]
        post = r.commentPost.get_absolute_url()
        message ='На твой отклик ответили.'
        send_email(user, email, post, message)


@receiver(post_save, sender=Response)
def send_response(instance, **kwargs):
    id = instance.id
    print(id)
    r = Response.objects.get(id=id)
    user = r.commentPost.author.username
    email = [r.commentPost.author.email]
    post = r.commentPost.get_absolute_url()
    message = 'Вам оставили отклик.'
    send_email(user, email, post, message)


@receiver(post_save, sender=User)
def send_response(created,instance, **kwargs):
    if created:
        p=AuthUser.objects.create(user=instance)

        # id = instance.id
        # r = Response.objects.get(id=id)
        # user = r.commentPost.author.username
        email = [instance.email]
        # post = r.commentPost.get_absolute_url()
        # message = 'Вам оставили отклик.'
        msg = EmailMultiAlternatives(
            subject='Код авторизации',
            body=f'Код авторизации {p.uuid}',  # это то же, что и message
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=email,  # это то же, что и recipients_list
        )
        msg.send()  # отсылаем


