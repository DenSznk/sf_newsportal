from django.contrib.auth.models import User
from django.db.models.signals import m2m_changed, pre_save, post_save
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives, send_mail
import datetime

from django.template.loader import render_to_string

from .models import Post, Category


@receiver(m2m_changed, sender=Post.category.throut)
def notify_subscription(sender, instance, created, *args, **kwargs):
    if created:
        send_mail(
            subject=f'Hello {instance.user.username}',
            message=f'new post was added in {Post.category}',
            from_email='densznk@gmail.com',
            recipient_list=User.email
        )
