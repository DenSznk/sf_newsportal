from django.contrib.auth.models import User
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives, send_mail
from django.template.loader import render_to_string

from news_portal import settings
from .tasks import notify_subscriber_celery
from .models import Post


@receiver(m2m_changed, sender=Post.category.through)
def notify_subscribers(instance, action,  *args, **kwargs):
    if action == 'post_add':
        users_emails = [
            user.email
            for category in instance.category.all()
            for user in category.subscribers.all()
        ]
        for email in users_emails:
            user = User.objects.get(email=email)
            html_content = render_to_string('account/email/notify_user.html', {'post_detail': instance}, )

            subject = f'Hello {user.username} a lot of spam is waiting for you '

            from_email = settings.EMAIL_FROM
            notify_subscriber_celery.delay(subject, from_email, email, html_content)

    # subscribers = instance.category.values(
    #     'subscribers__email', 'subscribers__username'
    # )
    # for subscriber in subscribers:
    #     html_content = render_to_string(
    #         'notify_user.html',
    #         {
    #             'post_detail': instance,
    #             'username': subscriber.get("subscribers__username")
    #         }
    #     )
    # msg = EmailMultiAlternatives(
    #     subject=instance.header_news,
    #     body=instance.post_text,
    #     to=[subscriber.get("subscribers__email")]
    # )
    # msg.attach_alternative(html_content, 'text/html')
    # msg.send()
    # notify_subscriber_celery.delay(subscriber, html_content)
