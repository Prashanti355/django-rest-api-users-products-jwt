from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from apps.users.models import User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    model = User

    list_display = (
        "id",
        "email",
        "username",
        "first_name",
        "last_name",
        "role",
        "is_active",
        "is_deleted",
        "email_verified",
        "created_at",
    )

    list_filter = (
        "role",
        "is_active",
        "is_deleted",
        "email_verified",
        "is_staff",
        "is_superuser",
    )

    search_fields = (
        "email",
        "username",
        "first_name",
        "last_name",
    )

    ordering = ("-created_at",)

    fieldsets = DjangoUserAdmin.fieldsets + (
        (
            "Profile information",
            {
                "fields": (
                    "profile_picture",
                    "nationality",
                    "occupation",
                    "date_of_birth",
                    "contact_phone_number",
                    "gender",
                )
            },
        ),
        (
            "Address information",
            {
                "fields": (
                    "address",
                    "address_number",
                    "address_interior_number",
                    "address_complement",
                    "address_neighborhood",
                    "address_zip_code",
                    "address_city",
                    "address_state",
                )
            },
        ),
        (
            "Business status",
            {
                "fields": (
                    "role",
                    "email_verified",
                    "email_verified_at",
                    "is_deleted",
                    "deleted_at",
                )
            },
        ),
        (
            "Audit",
            {
                "fields": (
                    "created_at",
                    "modified_at",
                )
            },
        ),
    )

    readonly_fields = (
        "created_at",
        "modified_at",
        "email_verified_at",
        "deleted_at",
    )
