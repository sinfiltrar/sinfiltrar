from django.contrib import admin
from issuers.models import Issuer, IssuerEmail


@admin.register(Issuer)
class IssuerAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'status', 'created_at', )
    list_filter = ('status', )
    list_search = ('name', 'slug', 'info', )
    date_hierarchy = 'created_at'


@admin.register(IssuerEmail)
class IssuerEmailAdmin(admin.ModelAdmin):
    list_display = ('id', 'email')
