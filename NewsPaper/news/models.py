from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.urls import reverse
from django.core.cache import cache


class Author(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE)
    author_rating = models.IntegerField(default=0)

    def update_rating(self):
        '''Рейтинг каждой статьи автора.'''
        rating_author_posts = Post.objects.filter(author=self).aggregate(r_ap=Coalesce(Sum('post_rating'), 0))['r_ap']

        '''Рейтинг всех комментариев автора.'''
        rating_author_comments = \
            Comment.objects.filter(comment_by_user=self.author).aggregate(r_ac=Coalesce(Sum('comment_rating'), 0))[
                'r_ac']

        '''Рейтинг всех комментариев к статьям автора.'''
        rating_comments_to_author_posts = Comment.objects.filter(comment_in_post__author=self).aggregate(
            r_ctap=Coalesce(Sum('comment_rating'), 0))['r_ctap']

        self.author_rating = rating_author_posts * 3 + rating_author_comments + rating_comments_to_author_posts
        self.save()

    def __str__(self):
        return self.author.username


class Category(models.Model):
    category_name = models.CharField(max_length=100, unique=True)
    subscribers = models.ManyToManyField(User,
                                         through='CategorySubscribers',
                                         related_name='subscribed_categories',
                                         blank=True)

    def __str__(self):
        return self.category_name


class CategorySubscribers(models.Model):
    subscriber = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)


class Post(models.Model):
    article = 'ARTC'
    news = 'NEWS'

    POSITIONS = [
        (article, 'Статья'),
        (news, 'Новости')
    ]

    post_title = models.CharField(max_length=255, unique=True)
    post_body = models.TextField()
    post_rating = models.IntegerField(default=0)
    post_content = models.CharField(max_length=4,
                                    choices=POSITIONS)
    post_creation_datetime = models.DateTimeField(auto_now_add=True)

    author = models.ForeignKey('Author', on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category, through='PostCategory', related_name='posts_categories')

    def preview(self):
        return self.post_body[:124] + '...' if len(self.post_body) > 124 else self.post_body

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete(f'post-{self.id}')

    def like(self):
        self.post_rating += 1
        self.save()

    def dislike(self):
        self.post_rating -= 1
        self.save()


class PostCategory(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)


class Comment(models.Model):
    comment_text = models.TextField()
    comment_creation_datetime = models.DateTimeField(auto_now_add=True)
    comment_rating = models.IntegerField(default=0)

    comment_in_post = models.ForeignKey('Post', on_delete=models.CASCADE)
    comment_by_user = models.ForeignKey(User, on_delete=models.CASCADE)

    def like(self):
        self.comment_rating += 1
        self.save()

    def dislike(self):
        self.comment_rating -= 1
        self.save()
