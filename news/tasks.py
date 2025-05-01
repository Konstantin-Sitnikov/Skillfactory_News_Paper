import datetime
from django_apscheduler.models import DjangoJobExecution
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from .models import Author, Category, Post
from NewsPaper.settings import SITE_URL, DEFAULT_FROM_EMAIL

from celery import shared_task

@shared_task()
def send_notifications(preview, pk, titel, subscribers):

    """Отправка сообщений в почту с новой новостью в категории"""

    html_content = render_to_string(
        'post_created_email.html',
        {
            'text': preview,
            'link': f'{SITE_URL}/{pk}'

        }
    )
    msg = EmailMultiAlternatives(
        subject=titel,
        body='',
        from_email=DEFAULT_FROM_EMAIL,
        to=subscribers

    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


@shared_task()
def updating_count_post():

    """Задача для сброса суточного лимита публикаций"""

    authors = Author.objects.all()
    for author in authors:
        author.get_count_null()



@shared_task()
def weekly_newsletter():

    """Еженедельная рассылка новостей подписчикам"""

    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=7)
    post = Post.objects.filter(date_time__gte = last_week)
    categories = set(post.values_list('category__category', flat=True))
    subscribers = set(Category.objects.filter(category__in=categories).values_list('subscribers__email', flat=True))

    html_content = render_to_string(
        'weekly_newsletter.html',
        {
            'link': SITE_URL,
            'posts': post
        }
    )

    msg = EmailMultiAlternatives(
        subject='Статьи за неделю',
        body='',
        from_email=DEFAULT_FROM_EMAIL,
        to=subscribers

    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


#
# # функция, которая будет удалять неактуальные задачи
# def delete_old_job_executions(max_age=604_800):
#     """This job deletes all apscheduler job executions older than `max_age` from the database."""
#     DjangoJobExecution.objects.delete_old_job_executions(max_age)
#
