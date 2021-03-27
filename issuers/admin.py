from django.contrib import admin
from issuers.models import Issuer, IssuerEmail

@admin.register(Issuer)
class IssuerAdmin(admin.ModelAdmin):
	list_display = ('id', 'slug', 'name')


@admin.register(IssuerEmail)
class IssuerEmailAdmin(admin.ModelAdmin):
	list_display = ('id', 'email')
