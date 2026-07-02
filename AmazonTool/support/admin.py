from django.contrib import admin
from .models import SupportTicket


@admin.register(SupportTicket)
class SupportTicketAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "vendor",
        "category",
        "subject",
        "status",
        "created_at",
    )

    list_filter = ("category", "status", "created_at")
    search_fields = ("subject", "message", "vendor__name")
    ordering = ("-created_at",)