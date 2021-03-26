from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<slug:slug>', views.one, name='one'),
    path('<slug:slug>/docs', views.docs, name='docs'),
];
