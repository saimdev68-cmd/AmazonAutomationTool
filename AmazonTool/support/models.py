from django.db import models
from seller.models import Seller
from accounts.models import User

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

    seller = models.ForeignKey(Seller,on_delete=models.CASCADE,related_name="supports")

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
        return f"{self.seller} - {self.subject}"
    
class AuditLog(models.Model):
    class Category(models.TextChoices):
        ACCOUNT = "account", "Account"
        DATA_IMPORT = "data_import", "Data Import"
        REPORT = "report", "Report"

    class Action(models.TextChoices):
        LOGIN = "login", "Login"
        LOGOUT = "logout", "Logout"

        CSV_UPLOAD = "csv_upload", "CSV Upload"
        CSV_DOWNLOAD = "csv_download", "CSV Download"

        REPORT_DOWNLOAD = "report_download", "Report Download"

        CREATE = "create", "Create"
        UPDATE = "update", "Update"
        DELETE = "delete", "Delete"

    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True,related_name="audit_logs",)
    user_email = models.EmailField()
    category = models.CharField(max_length=30,choices=Category.choices,)
    action = models.CharField(max_length=30,choices=Action.choices,)
    detail = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user_email} - {self.category} - {self.action}"