import logging

from django.conf import settings
from django.utils import timezone
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from news.models import Post, User

logger = logging.getLogger(__name__)


def my_job():
    print('hello from job')


def send_weekly_subscription_posts():
    week_ago = timezone.now() - timezone.timedelta(weeks=1)
    new_posts_1_week = Post.objects.filter(post_creation_datetime__gte=week_ago)
    subscribed_users = User.objects.filter(subscribed_categories__isnull=False).distinct()

    for subscriber in subscribed_users:
        subscribed_categories = subscriber.subscribed_categories.all()
        posts_to_send = new_posts_1_week.filter(categories__in=subscribed_categories).distinct()
        if posts_to_send.exists():
            html_content = render_to_string(
                'weekly_subscription_info.html',
                {'posts': posts_to_send, 'subscriber': subscriber}
            )
            msg = EmailMultiAlternatives(
                subject=f'Здравствуй, {subscriber.username}. Новинки за неделю!',
                body='',
                from_email='pwndatronic@yandex.ru',
                to=[subscriber.email]
            )
            msg.attach_alternative(html_content, 'text/html')
            try:
                msg.send(fail_silently=False)
            except Exception as e:
                print(f'Ошибка: {e}')


def delete_old_job_executions(max_age=1_209_600):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            my_job,
            trigger=CronTrigger(second="*/20"),
            id="my_job",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        # scheduler.add_job(
        #     send_weekly_subscription_posts,
        #     trigger=CronTrigger(
        #         day_of_week='mon',
        #         hour='12'
        #     ),
        #     id="send_weekly_subscription_posts_monday",
        #     max_instances=1,
        #     replace_existing=True,
        # )
        # logger.info("Added job 'my_job'.")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
