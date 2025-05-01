from django.dispatch import receiver
from django.db.models.signals import m2m_changed
from django.template.loader import render_to_string
from news.models import PostCategory
from django.core.mail import EmailMultiAlternatives
from NewsPaper.settings import SITE_URL, DEFAULT_FROM_EMAIL
from .tasks import send_notifications


@receiver(m2m_changed, sender=PostCategory)
def notify_about_new_post(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        categories = instance.category.all()
        subscribers_emails = []

        for cat in categories:
            subscribers = cat.subscribers.all()
            subscribers_emails +=[s.email for s in subscribers]

        send_notifications.apply_async([instance.preview(), instance.pk, instance.title_news, subscribers_emails]) #Асинхронный вызов функции для отправки сообщения

