from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone
from .models import Post, User


@shared_task()
def send_to_subscribers(post_id):
    post = Post.objects.get(id=post_id)
    categories = post.categories.all()
    subscribers = User.objects.filter(subscribed_categories__in=categories).distinct()
    for subscriber in subscribers:
        html_content = render_to_string(
            'subscription_info.html',
            {'new': post, 'subscriber': subscriber}
        )
        msg = EmailMultiAlternatives(
            subject=f'Здравствуй, {subscriber.username}. Новая статья в твоём любимом разделе!',
            body='',
            from_email='pwndatronic@yandex.ru',
            to=[subscriber.email]
        )
        msg.attach_alternative(html_content, 'text/html')
        try:
            msg.send(fail_silently=False)
        except Exception as e:
            print(f'Ошибка: {e}')


@shared_task()
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
