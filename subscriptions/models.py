from django.db import models


class Subscription(models.Model):
    user = models.ForeignKey(
        'users.User',
        related_name='subscriptions',
        verbose_name='Подписчик',
        on_delete=models.CASCADE,
    )
    tags = models.ManyToManyField(
        'newsportal.Tag',
        related_name='subscriptions',
        through='subscriptions.SubscriptionTag',
    )


class SubscriptionTag(models.Model):
    tag = models.ForeignKey(
        'newsportal.Tag',
        on_delete=models.CASCADE,
        primary_key=True,
    )
    subscription = models.ForeignKey(
        'subscriptions.Subscription',
        on_delete=models.CASCADE,
        primary_key=True,
    )
