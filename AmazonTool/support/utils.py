# utils/audit.py

from .models import AuditLog


def create_audit_log(user, category, action, detail=""):
    AuditLog.objects.create(
        user=user if user.is_authenticated else None,
        user_email=user.email if user.is_authenticated else "",
        category=category,
        action=action,
        detail=detail,
    )