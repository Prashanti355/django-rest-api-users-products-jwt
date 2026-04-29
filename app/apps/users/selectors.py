from django.contrib.auth import get_user_model

User = get_user_model()


def get_active_users():
    return User.objects.filter(is_deleted=False)


def get_user_by_id(user_id):
    return get_active_users().get(id=user_id)


def get_deleted_users():
    return User.objects.filter(is_deleted=True)