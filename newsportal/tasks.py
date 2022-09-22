from datetime import datetime

from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from news_portal import settings
from newsportal.models import Category, Post


@shared_task
def notify_subscriber_celery(subject, from_email, email, html_content):
    msg = EmailMultiAlternatives(
        subject=subject,
        from_email=from_email,
        to=[email]
    )

    msg.attach_alternative(html_content, "text/html")
    msg.send()


@shared_task
def celery_week_mails():
    time_delta = datetime.timedelta(7)
    start_date = datetime.datetime.utcnow() - time_delta
    end_date = datetime.datetime.utcnow()

    posts = Post.objects.filter(post_data__range=(start_date, end_date))

    for category in Category.objects.all():
        html_content = render_to_string('account/email/weekly_spam.html',
                                        {'posts': posts, 'category': category}, )
        msg = EmailMultiAlternatives(
            subject=f'Weekly spam is waiting for you',
            body='News',
            from_email=settings.EMAIL_FROM,
            to=category.get_subscribers_emails())
        msg.attach_alternative(html_content, "text/html")
        msg.send()
