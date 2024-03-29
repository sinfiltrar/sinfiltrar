"""sinfiltrar URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from django.contrib.sitemaps.views import sitemap
from .sitemap import MainSitemap
from stats.sitemap import StatsSitemap
from docs.sitemap import DocsSitemap
from issuers.sitemap import IssuersSitemap

sitemaps = {
    'main': MainSitemap,
    'stats': StatsSitemap,
    'docs': DocsSitemap,
    'issuers': IssuersSitemap,
}

urlpatterns = [
    path('', include('docs.urls')),
    path('', include('issuers.urls')),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('about/', TemplateView.as_view(template_name='about.html'), name='about'),
    path('stats/', include('stats.urls')),
    path('us/', TemplateView.as_view(template_name='us.html'), name='us'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap')
]