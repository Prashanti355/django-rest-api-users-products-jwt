from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "password",
        )

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "role",
            "is_active",
        )


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ("password",)


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ("password", "id", "created_at", "modified_at")

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
    
class UserRoleUpdateSerializer(serializers.Serializer):
    role = serializers.ChoiceField(choices=User.Role.choices)