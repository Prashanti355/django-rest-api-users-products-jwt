import django_filters

from apps.audit.models import AuditLog


class AuditLogFilter(django_filters.FilterSet):
    actor_email = django_filters.CharFilter(
        field_name="actor_email",
        lookup_expr="icontains",
    )
    action = django_filters.ChoiceFilter(choices=AuditLog.Action.choices)
    entity_type = django_filters.ChoiceFilter(choices=AuditLog.EntityType.choices)
    status = django_filters.ChoiceFilter(choices=AuditLog.Status.choices)
    created_after = django_filters.DateTimeFilter(
        field_name="created_at",
        lookup_expr="gte",
    )
    created_before = django_filters.DateTimeFilter(
        field_name="created_at",
        lookup_expr="lte",
    )

    class Meta:
        model = AuditLog
        fields = (
            "actor_email",
            "action",
            "entity_type",
            "status",
            "created_after",
            "created_before",
        )
