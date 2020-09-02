# Generated by Django 2.2 on 2020-04-12 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0010_article_post'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='dislikes',
            field=models.IntegerField(default=0, verbose_name='Не нравится'),
        ),
        migrations.AddField(
            model_name='post',
            name='likes',
            field=models.IntegerField(default=0, verbose_name='Нравится'),
        ),
        migrations.DeleteModel(
            name='Article',
        ),
    ]