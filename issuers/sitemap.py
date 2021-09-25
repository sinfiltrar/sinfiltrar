from django.contrib.sitemaps import Sitemap
from issuers.models import Issuer

class IssuersSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5

    def items(self):
        return Issuer.objects.exclude(status=Issuer.status)

    def lastmod(self, obj):
        return obj.created_at