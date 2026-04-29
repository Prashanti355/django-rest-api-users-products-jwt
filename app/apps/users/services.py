from django.contrib.auth import get_user_model
from django.db import transaction

from apps.audit.models import AuditLog
from apps.audit.services import create_audit_log

User = get_user_model()


@transaction.atomic
def soft_delete_user(user, actor=None, request=None):
    user.soft_delete()

    create_audit_log(
        action=AuditLog.Action.USER_DELETE,
        entity_type=AuditLog.EntityType.USER,
        entity_id=user.id,
        actor=actor,
        detail=f"User soft deleted: {user.email}",
        request=request,
    )

    return user


@transaction.atomic
def restore_user(user, actor=None, request=None):
    user.restore()

    create_audit_log(
        action=AuditLog.Action.USER_RESTORE,
        entity_type=AuditLog.EntityType.USER,
        entity_id=user.id,
        actor=actor,
        detail=f"User restored: {user.email}",
        request=request,
    )

    return user


@transaction.atomic
def change_user_role(user, role, actor=None, request=None):
    valid_roles = {choice[0] for choice in User.Role.choices}

    if role not in valid_roles:
        raise ValueError("Invalid role.")

    previous_role = user.role
    user.role = role
    user.save(update_fields=["role", "modified_at"])

    create_audit_log(
        action=AuditLog.Action.USER_UPDATE_ROLE,
        entity_type=AuditLog.EntityType.USER,
        entity_id=user.id,
        actor=actor,
        detail=f"Role changed from {previous_role} to {role} for user {user.email}",
        request=request,
    )

    return user
