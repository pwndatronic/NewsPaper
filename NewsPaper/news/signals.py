from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Post
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


# @receiver(post_save, sender=Post)
def send_to_subscribers(sender, instance, created, **kwargs):
    if not created:
        categories = instance.categories.all()
        subscribers = User.objects.filter(subscribed_categories__in=categories).distinct()
        for subscriber in subscribers:
            html_content = render_to_string(
                'subscription_info.html',
                {'new': instance, 'subscriber': subscriber}
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
