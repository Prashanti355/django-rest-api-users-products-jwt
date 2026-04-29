from django.contrib import admin

from apps.products.models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "product_key",
        "product_type",
        "price",
        "stock",
        "is_active",
        "is_deleted",
        "owner",
        "created_at",
    )

    list_filter = (
        "product_type",
        "is_active",
        "is_deleted",
        "created_at",
    )

    search_fields = (
        "name",
        "description",
        "product_key",
        "owner__email",
    )

    readonly_fields = (
        "id",
        "created_at",
        "modified_at",
        "deleted_at",
    )