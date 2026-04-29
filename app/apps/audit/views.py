from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.audit import selectors
from apps.audit.permissions import IsAdminRole
from apps.audit.serializers import AuditLogSerializer


@extend_schema_view(
    list=extend_schema(tags=["Audit Logs"]),
    retrieve=extend_schema(tags=["Audit Logs"]),
)
class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = AuditLogSerializer
    permission_classes = [IsAuthenticated, IsAdminRole]

    def get_queryset(self):
        return selectors.filter_audit_logs(
            actor_email=self.request.query_params.get("actor_email"),
            action=self.request.query_params.get("action"),
            entity_type=self.request.query_params.get("entity_type"),
            status=self.request.query_params.get("status"),
        )
