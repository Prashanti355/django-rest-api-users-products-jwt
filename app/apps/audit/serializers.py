from rest_framework import serializers

from apps.audit.models import AuditLog


class AuditLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditLog
        fields = (
            "id",
            "actor_email",
            "action",
            "entity_type",
            "entity_id",
            "status",
            "detail",
            "request_id",
            "request_method",
            "request_path",
            "created_at",
        )
