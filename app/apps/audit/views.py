from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated

from apps.audit import selectors
from apps.audit.filters import AuditLogFilter
from apps.audit.permissions import IsAdminRole
from apps.audit.serializers import AuditLogSerializer


@extend_schema_view(
    list=extend_schema(tags=["Audit Logs"]),
    retrieve=extend_schema(tags=["Audit Logs"]),
)
class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = AuditLogSerializer
    permission_classes = [IsAuthenticated, IsAdminRole]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = AuditLogFilter
    search_fields = ["actor_email", "detail", "request_path", "entity_id"]
    ordering_fields = ["created_at", "action", "entity_type", "status", "actor_email"]
    ordering = ["-created_at"]

    def get_queryset(self):
        return selectors.filter_audit_logs(
            actor_email=self.request.query_params.get("actor_email"),
            action=self.request.query_params.get("action"),
            entity_type=self.request.query_params.get("entity_type"),
            status=self.request.query_params.get("status"),
        )
