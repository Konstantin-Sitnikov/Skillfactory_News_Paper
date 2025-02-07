# Generated by Django 5.1.5 on 2025-02-07 06:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0004_rename__rating_autor_author_rating_autor'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='_rating_comments',
            new_name='rating_comments',
        ),
        migrations.RemoveField(
            model_name='post',
            name='_rating_post',
        ),
        migrations.AddField(
            model_name='post',
            name='rating_post',
            field=models.IntegerField(default=0),
        ),
    ]
