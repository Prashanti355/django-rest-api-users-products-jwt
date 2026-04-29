from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from apps.users import selectors, services
from apps.users.permissions import IsAdminRole, IsSelfOrAdmin
from apps.users.serializers import (
    UserCreateSerializer,
    UserDetailSerializer,
    UserListSerializer,
    UserRoleUpdateSerializer,
    UserUpdateSerializer,
)

User = get_user_model()


@extend_schema_view(
    list=extend_schema(tags=["Users"]),
    retrieve=extend_schema(tags=["Users"]),
    create=extend_schema(tags=["Users"]),
    update=extend_schema(tags=["Users"]),
    partial_update=extend_schema(tags=["Users"]),
    destroy=extend_schema(tags=["Users"]),
    restore=extend_schema(tags=["Users"]),
    set_role=extend_schema(tags=["Users"]),
    me=extend_schema(tags=["Users"]),
)
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action == "create":
            return UserCreateSerializer

        if self.action == "list":
            return UserListSerializer

        if self.action in ["update", "partial_update"]:
            return UserUpdateSerializer

        if self.action == "set_role":
            return UserRoleUpdateSerializer

        return UserDetailSerializer

    def get_permissions(self):
        if self.action == "create":
            return [AllowAny()]

        if self.action == "list":
            return [IsAdminRole()]

        if self.action in ["retrieve", "update", "partial_update"]:
            return [IsAuthenticated(), IsSelfOrAdmin()]

        if self.action in ["destroy", "restore", "set_role"]:
            return [IsAuthenticated(), IsAdminRole()]

        if self.action == "me":
            return [IsAuthenticated()]

        return [IsAuthenticated()]

    def get_queryset(self):
        return selectors.get_active_users()

    def perform_destroy(self, instance):
        services.soft_delete_user(
            instance,
            actor=self.request.user,
            request=self.request,
        )

    @action(detail=True, methods=["patch"])
    def restore(self, request, pk=None):
        user = User.objects.get(id=pk)
        user = services.restore_user(
            user,
            actor=request.user,
            request=request,
        )
        return Response(UserDetailSerializer(user).data)

    @action(detail=True, methods=["patch"])
    def set_role(self, request, pk=None):
        serializer = UserRoleUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = selectors.get_user_by_id(pk)
        user = services.change_user_role(
            user,
            serializer.validated_data["role"],
            actor=request.user,
            request=request,
        )

        return Response(UserDetailSerializer(user).data)

    @action(detail=False, methods=["get", "patch"])
    def me(self, request):
        if request.method == "PATCH":
            serializer = UserUpdateSerializer(
                request.user,
                data=request.data,
                partial=True,
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

        serializer = UserDetailSerializer(request.user)
        return Response(serializer.data)