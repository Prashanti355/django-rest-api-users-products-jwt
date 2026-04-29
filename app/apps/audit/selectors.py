from apps.audit.models import AuditLog


def get_audit_logs():
    return AuditLog.objects.all()


def filter_audit_logs(
    *,
    actor_email=None,
    action=None,
    entity_type=None,
    status=None,
):
    qs = get_audit_logs()

    if actor_email:
        qs = qs.filter(actor_email__icontains=actor_email)

    if action:
        qs = qs.filter(action=action)

    if entity_type:
        qs = qs.filter(entity_type=entity_type)

    if status:
        qs = qs.filter(status=status)

    return qs
