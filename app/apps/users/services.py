from django.contrib.auth import get_user_model
from django.db import transaction

User = get_user_model()


@transaction.atomic
def soft_delete_user(user):
    user.soft_delete()
    return user


@transaction.atomic
def restore_user(user):
    user.restore()
    return user


@transaction.atomic
def change_user_role(user, role):
    valid_roles = {choice[0] for choice in User.Role.choices}

    if role not in valid_roles:
        raise ValueError("Invalid role.")

    user.role = role
    user.save(update_fields=["role", "modified_at"])
    return user