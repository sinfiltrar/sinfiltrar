from django.contrib.sitemaps import Sitemap
from docs.models import Doc

class DocsSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5

    def items(self):
        return Doc.objects.exclude(issuer=None)

    def lastmod(self, obj):
        return obj.issued_at