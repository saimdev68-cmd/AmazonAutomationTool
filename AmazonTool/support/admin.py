from django.contrib import admin
from .models import SupportTicket , AuditLog


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

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = (
        "created_at",
        "user_email",
        "category",
        "action",
        "detail",
    )

    list_filter = (
        "category",
        "action",
        "created_at",
    )

    search_fields = (
        "user_email",
        "detail",
    )

    readonly_fields = (
        "created_at",
    )