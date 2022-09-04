from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum
from django.core.mail import send_mail

from django.conf import settings


from newsportal.resources import CATEGORY_NAME


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username

    def update_rating(self):
        rating_post_author = self.post_set.all().aggregate(sum=Sum('rating') * 3)['sum']
        rating_comment = self.user.comment_set.all().aggregate(sum=Sum('comment_rating'))['sum']
        rating_comment_post = Post.objects.filter(author=self).aggregate(sum=Sum('rating'))['sum']
        self.sum_rating = rating_post_author + rating_comment + rating_comment_post
        self.save()


class Category(models.Model):
    category_name = models.CharField(max_length=155, unique=True)
    subscribers = models.ManyToManyField(User, through='UserCategory')

    def __str__(self):
        return self.category_name

    def is_user_subscribed(self, user_id: int) -> bool:
        return self.subscribers.filter(id=user_id).exists()

    def get_subscribers_emails(self):
        # result = set()
        # for user in self.subscribers.all():
        #     result.add(user.email)
        return self.subscribers.all().values_list('user__email', flat=True)


class Post(models.Model):
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE
    )
    choice_category = models.CharField(
        max_length=2,
        choices=CATEGORY_NAME
    )
    date_time_auto = models.DateTimeField(
        auto_now_add=True
    )
    category = models.ManyToManyField(
        Category,
        through='PostCategory',
        verbose_name='Categories'
    )
    header_news = models.CharField(
        max_length=155
    )
    post_text = models.TextField()
    rating = models.IntegerField(
        default=0
    )

    def __str__(self):
        return f'{self.header_news}. {self.post_text}'

    def add_like(self):
        self.rating += 1
        self.save()

    def add_dislike(self):
        self.rating -= 1
        self.save()

    def get_preview(self):
        preview = f"{self.post_text[:124]}"
        if len(preview) > 124:
            preview += '...'
        return preview

    def get_absolute_url(self):
        return f'/posts/{self.id}'

    def save(self, *args, **kwargs):
        saved_obj = super().save(*args, **kwargs)
        
        # проверить если пост создаётся (self.pk == None - значит создаётся)
        # отправить письмо с содержанием заголовка создался новый пост в категори тра ля ля
        return saved_obj


class Comment(models.Model):
    user_one_to_many = models.ForeignKey(User, on_delete=models.CASCADE)
    post_one_to_many = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_text = models.TextField()
    comment_date = models.DateTimeField(auto_now_add=True)
    comment_rating = models.IntegerField(default=0)

    def __str__(self):
        return self.comment_text.title()

    def add_like(self):
        self.comment_rating += 1
        self.save()

    def add_dislike(self):
        self.comment_rating -= 1
        self.save()


# TODO переименовать в subscription
class UserCategory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def save(self, *args, **kwargs) -> None:
        saved_object = super().save(*args, **kwargs)

        send_mail(
            subject=f'Подписка новости {self.category.category_name}',
            message='Спасибо что подписались на новости по теме....',
            recipient_list=[self.user.email],
            from_email=settings.EMAIL_FROM,
        )

        return saved_object
        

    class Meta:
        unique_together = (
            ('user', 'category'),
        )


class PostCategory(models.Model):
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
