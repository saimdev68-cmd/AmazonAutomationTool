from django.contrib import admin
from .models import SupportTicket


@admin.register(SupportTicket)
class SupportTicketAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "seller",
        "category",
        "subject",
        "status",
        "created_at",
    )

    list_filter = ("category", "status", "created_at")
    search_fields = ("subject", "message", "seller__name")
    ordering = ("-created_at",)