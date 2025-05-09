from django.contrib import admin
from .models import Post, Category, Comment, Author, CategorySubscribers


class PostAdmin(admin.ModelAdmin):
    list_display = ('post_title',
                    'post_rating',
                    'post_content',
                    'author')
    list_filter = ('post_title',
                   'post_rating',
                   'author')
    search_fields = ('post_title',
                     'author__author__username')


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('author',
                    'author_rating')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('comment_creation_datetime',
                    'comment_by_user',
                    'comment_rating',
                    'comment_in_post')
    list_filter = ('comment_in_post',
                   'comment_by_user',
                   'comment_rating',
                   'comment_creation_datetime')
    search_fields = ('comment_in_post__post_title',
                     'comment_by_user__username',
                     'comment_creation_datetime')


class CategorySubscribersInLine(admin.TabularInline):
    model = CategorySubscribers
    extra = 1

# class CategorySubscribersInLine(admin.StackedInline):
#     model = CategorySubscribers
#     extra = 1


class CategoryAdmin(admin.ModelAdmin):
    inlines = [CategorySubscribersInLine]
    list_display = ('category_name',
                    'display_subscribers_usernames',)
    search_fields = ('subscribers__username',)

    @admin.display(description='Subscribers usernames')
    def display_subscribers_usernames(self, obj):
        return ', '.join([str(user.username) for user in obj.subscribers.all()])


admin.site.register(Category, CategoryAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Post, PostAdmin)
