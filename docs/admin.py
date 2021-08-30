from django.contrib import admin
from docs.models import Doc


@admin.register(Doc)
class DocAdmin(admin.ModelAdmin):
    date_hierarchy = 'issued_at'
    list_display = ('title', 'from_email', 'issued_at', 'issuer')
    list_filter = ('issuer', )
