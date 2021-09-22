from django.urls import path
from . import views


urlpatterns = [
    path('', views.index),
    path('query/weekly-docs', views.weekly_docs, name='query_weekly-docs')
]
