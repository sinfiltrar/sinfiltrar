from django.contrib.sitemaps import Sitemap
from django.urls import reverse

class StatsSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5

    def items(self):
        return ['stats']

    def location(self, item):
        return reverse(item)