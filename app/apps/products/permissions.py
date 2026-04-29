from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrStaff(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role in ("ADMIN", "STAFF")
        )


class IsAdminOnly(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == "ADMIN"
        )


class CanViewProduct(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.role == "ADMIN":
            return True

        if request.user.role == "STAFF":
            return True

        return obj.is_active and not obj.is_deleted