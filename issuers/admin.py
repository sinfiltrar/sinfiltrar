from django.contrib import admin
from issuers.models import Issuer, IssuerEmail


@admin.register(Issuer)
class IssuerAdmin(admin.ModelAdmin):
	pass


@admin.register(IssuerEmail)
class IssuerEmailAdmin(admin.ModelAdmin):
	pass
