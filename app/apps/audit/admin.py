from django.contrib import admin

from apps.audit.models import AuditLog


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "actor_email",
        "action",
        "entity_type",
        "entity_id",
        "status",
        "request_method",
        "request_path",
        "created_at",
    )

    list_filter = (
        "action",
        "entity_type",
        "status",
        "created_at",
    )

    search_fields = (
        "actor_email",
        "entity_id",
        "detail",
        "request_path",
    )

    readonly_fields = (
        "id",
        "created_at",
    )