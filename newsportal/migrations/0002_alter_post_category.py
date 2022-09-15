# Generated by Django 4.0.6 on 2022-08-19 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newsportal', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='category',
            field=models.ManyToManyField(through='newsportal.PostCategory', to='newsportal.category', verbose_name='Categories'),
        ),
    ]
