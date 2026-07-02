from django.db import models
from vendor.models import Vendor


class SupportTicket(models.Model):

    class Category(models.TextChoices):
        GENERAL_INQUIRY = "general_inquiry", "General Inquiry"
        BILLING = "billing", "Billing"
        TECHNICAL_ISSUE = "technical_issue", "Technical Issue"
        PPC_MANAGEMENT = "ppc_management", "PPC Management"
        DATA_IMPORT_EXPORT = "data_import_export", "Data Import / Export"

    class Status(models.TextChoices):
        OPEN = "open", "Open"
        IN_PROGRESS = "in_progress", "In Progress"
        RESOLVED = "resolved", "Resolved"
        CLOSED = "closed", "Closed"

    vendor = models.ForeignKey(
        Vendor,
        on_delete=models.CASCADE,
        related_name="support_tickets"
    )

    category = models.CharField(
        max_length=50,
        choices=Category.choices
    )

    subject = models.CharField(max_length=255)
    message = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.OPEN
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.vendor} - {self.subject}"