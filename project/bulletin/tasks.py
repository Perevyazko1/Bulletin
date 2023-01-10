from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


@shared_task()
def send_email(user, email, post, message):
    html_content = render_to_string(
        'send_response.html',
        {
            'link': settings.SITE_URL,
            'post': post,
            'user': user,
            'message': message
        }
    )

    msg = EmailMultiAlternatives(
        subject=message,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=email,
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()
