# import logging
#
# from apscheduler.schedulers.blocking import BlockingScheduler
# from apscheduler.triggers.cron import CronTrigger
# from django.core.management.base import BaseCommand
# from django_apscheduler.jobstores import DjangoJobStore
#
# from news.tasks import updating_count_post, delete_old_job_executions, weekly_newsletter
# logger = logging.getLogger(__name__)
#
#
# class Command(BaseCommand):
#     help = "Runs apscheduler."
#
#     def handle(self, *args, **options):
#         scheduler = BlockingScheduler()
#         scheduler.add_jobstore(DjangoJobStore(), "default")
#
#         #обновление количества публикаций в день
#         scheduler.add_job(
#             updating_count_post,
#             trigger=CronTrigger(hour="13", minute="22"),
#
#             id="updating_count_post",  # уникальный айди
#             max_instances=1,
#             replace_existing=True,
#         )
#         logger.info("Added job 'updating_count_post'.")
#
#         #еженедельная рассылка новостей
#         scheduler.add_job(
#             weekly_newsletter,
#             trigger=CronTrigger(day_of_week="mon", hour="13", minute="22"),
#             id="weekly_newsletter",
#             max_instances=1,
#             replace_existing=True,
#         )
#         logger.info("Added job 'weekly_newsletter'.")
#
#
#         scheduler.add_job(
#             delete_old_job_executions,
#             trigger=CronTrigger(
#                 day_of_week="mon", hour="00", minute="00"
#             ),
#             id="delete_old_job_executions",
#             max_instances=1,
#             replace_existing=True,
#         )
#         logger.info(
#             "Added weekly job: 'delete_old_job_executions'."
#         )
#
#         try:
#             logger.info("Starting scheduler...")
#             scheduler.start()
#         except KeyboardInterrupt:
#             logger.info("Stopping scheduler...")
#             scheduler.shutdown()
#             logger.info("Scheduler shut down successfully!")