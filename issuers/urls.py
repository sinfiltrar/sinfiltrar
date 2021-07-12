from django.urls import include, path
from rest_framework import routers
from . import views


router = routers.SimpleRouter()
router.register(r'', views.ApiIssuerViewSet)

urlpatterns = [
    path('api/issuers/', include(router.urls)),
    path('issuers/', views.index, name='issuers_index'),
    path('issuers/<slug>/', views.one, name='issuers_one'),
]
