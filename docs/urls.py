from django.urls import include, path
from . import views
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'', views.ApiDocViewSet)

urlpatterns = [
    path('api/docs/', include(router.urls)),
    path('', views.index, name='docs_index'),
    path('docs/<slug>/', views.one, name='docs_one'),
]
