from apps.audit.models import AuditLog


def create_audit_log(
    *,
    action,
    entity_type,
    status=AuditLog.Status.SUCCESS,
    actor=None,
    entity_id=None,
    detail="",
    request=None,
):
    actor_email = None

    if actor and getattr(actor, "is_authenticated", False):
        actor_email = actor.email

    request_id = None
    request_method = None
    request_path = None

    if request:
        request_id = getattr(request, "request_id", None)
        request_method = request.method
        request_path = request.path

    return AuditLog.objects.create(
        actor=actor if actor and getattr(actor, "is_authenticated", False) else None,
        actor_email=actor_email,
        action=action,
        entity_type=entity_type,
        entity_id=str(entity_id) if entity_id else None,
        status=status,
        detail=detail,
        request_id=request_id,
        request_method=request_method,
        request_path=request_path,
    )