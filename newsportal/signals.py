from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from .models import Post


@receiver(m2m_changed, sender=Post.category.through)
def notify_subscribers(sender, instance, *args, **kwargs):
    subscribers = instance.category.values(
        'subscribers__email', 'subscribers__username'
    )
    for subscriber in subscribers:
        html_content = render_to_string(
            'notify_user.html',
            {
                'post_detail': instance,
                'username': subscriber.get("subscribers__username")
            }
        )
        msg = EmailMultiAlternatives(
            subject=instance.header_news,
            body=instance.post_text,
            to=[subscriber.get("subscribers__email")]
        )
        msg.attach_alternative(html_content, 'text/html')
        msg.send()

