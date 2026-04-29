from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from apps.audit.models import AuditLog
from apps.audit.services import create_audit_log


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            email = request.data.get("email")

            create_audit_log(
                action=AuditLog.Action.LOGIN,
                entity_type=AuditLog.EntityType.AUTH,
                actor=None,  # aún no tenemos user autenticado aquí directamente
                detail=f"Login success for {email}",
                request=request,
            )

        else:
            create_audit_log(
                action=AuditLog.Action.LOGIN,
                entity_type=AuditLog.EntityType.AUTH,
                status=AuditLog.Status.FAILURE,
                actor=None,
                detail="Login failed",
                request=request,
            )

        return response


class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            create_audit_log(
                action=AuditLog.Action.TOKEN_REFRESH,
                entity_type=AuditLog.EntityType.AUTH,
                detail="Token refreshed",
                request=request,
            )

        return response
