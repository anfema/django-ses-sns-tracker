from django.contrib import admin

from .models import SESMailDelivery


@admin.register(SESMailDelivery)
class SESMailDeliveryAdmin(admin.ModelAdmin):
    list_display = ('recipient', 'sent_at', 'updated_at', 'state')
    list_filter = ('state',)
    readonly_fields = ('sent_at', 'updated_at')
    ordering = ('-updated_at',)
