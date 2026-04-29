import uuid

from django.conf import settings
from django.db import models


class AuditLog(models.Model):
    class Action(models.TextChoices):
        LOGIN = "LOGIN", "Login"
        TOKEN_REFRESH = "TOKEN_REFRESH", "Token refresh"

        USER_CREATE = "USER_CREATE", "User create"
        USER_UPDATE = "USER_UPDATE", "User update"
        USER_UPDATE_ROLE = "USER_UPDATE_ROLE", "User update role"
        USER_DELETE = "USER_DELETE", "User delete"
        USER_RESTORE = "USER_RESTORE", "User restore"

        PRODUCT_CREATE = "PRODUCT_CREATE", "Product create"
        PRODUCT_UPDATE = "PRODUCT_UPDATE", "Product update"
        PRODUCT_DELETE = "PRODUCT_DELETE", "Product delete"
        PRODUCT_RESTORE = "PRODUCT_RESTORE", "Product restore"

    class EntityType(models.TextChoices):
        AUTH = "AUTH", "Auth"
        USER = "USER", "User"
        PRODUCT = "PRODUCT", "Product"

    class Status(models.TextChoices):
        SUCCESS = "SUCCESS", "Success"
        FAILURE = "FAILURE", "Failure"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="audit_logs",
    )
    actor_email = models.EmailField(blank=True, null=True)

    action = models.CharField(max_length=40, choices=Action.choices)
    entity_type = models.CharField(max_length=40, choices=EntityType.choices)
    entity_id = models.CharField(max_length=100, blank=True, null=True)

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.SUCCESS,
    )

    detail = models.TextField(blank=True)
    request_id = models.CharField(max_length=100, blank=True, null=True)
    request_method = models.CharField(max_length=10, blank=True, null=True)
    request_path = models.CharField(max_length=255, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "audit_logs"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["actor_email"]),
            models.Index(fields=["action"]),
            models.Index(fields=["entity_type"]),
            models.Index(fields=["status"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        return f"{self.action} - {self.status} - {self.created_at}"
