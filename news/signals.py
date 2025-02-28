from django.dispatch import resiver
from django.db.models.signals import m2m_changet
from django.tempate.loader import render_to_string
from news.models import PostCategory
from NewsPaper.settings import SITE_URL

# def send_notifications(preview, pk, titel, subscribers):
#     html_content = render_to_string(
#         'post_created_email',
#         {
#             'text': preview,
#             'link': f'{SITE_URL}/{pk}'
#
#         }
#     )
#     msg = EmailMulti Alternatives(s)



@resiver(m2m_changet, sender=PostCategory)
def notify_about_new_post(sender, instanse, **kwargs):
    if kwargs['action'] == 'post_add':
        categories = instanse.category.all()
        subscribers_emails = []

        for cat in categories:
            subscribers = cat.subscribers.all()
            subscribers_emails +=[s.email for s in subscribers]


