from django.contrib.sitemaps import Sitemap
from django.urls import reverse

class MainSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5

    def items(self):
        return ['about', 'us']

    def location(self, item):
        return reverse(item)