from .views import IndexView
from django.urls import path
from django.views.decorators.cache import cache_page


urlpatterns = [
   path('', cache_page(60)(IndexView.as_view())),
]
