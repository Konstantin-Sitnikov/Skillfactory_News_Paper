import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPaper.settings')

app = Celery('mcdonalds')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
app.conf.broker_connection_retry_on_startup = True


app.conf.beat_schedule = {
    'every_day_updating_count_post_00.00': {
        'task': 'news.tasks.updating_count_post',
        'schedule': crontab(minute=0, hour=0),
    },

    'every_monday_weekly_newsletter': {
        'task': 'news.tasks.weekly_newsletter',
        'schedule': crontab(minute=0, hour=8, day_of_week='monday'),
    },
}



#day_of_week='monday'