from django.urls import path
from .views import *
from django.views.decorators.cache import cache_page


urlpatterns = [
    path('', cache_page(60)(NewsList.as_view()), name='news_list'),
    path('<int:id>', PostDetail.as_view(), name='post_detail'),
    path('search/', NewsSearch.as_view(), name='news_search'),
    path('news/create/', NewsCreate.as_view(), name='news_create'),
    path('news/<int:id>/update/', NewsUpdate.as_view(), name='news_update'),
    path('news/<int:id>/delete/', NewsDelete.as_view(), name='news_delete'),
    path('article/create/', ArticleCreate.as_view(), name='article_create'),
    path('article/<int:id>/update/', ArticleUpdate.as_view(), name='article_update'),
    path('article/<int:id>/delete/', ArticleDelete.as_view(), name='article_delete'),
    path('subscribe/<int:post_id>/', subscribe_to_categories, name='subscribe')
]
