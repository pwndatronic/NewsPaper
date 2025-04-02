import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPaper.settings')

app = Celery('NewsPaper')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'send_weekly_subscription_posts_mon_8am': {
        'task': 'news.tasks.send_weekly_subscription_posts',
        'schedule': crontab(hour='8', minute='0', day_of_week='monday'),
    }
}

app.autodiscover_tasks()
