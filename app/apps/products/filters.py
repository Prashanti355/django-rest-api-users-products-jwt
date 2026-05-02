import django_filters

from apps.products.models import Product


class ProductFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name="price", lookup_expr="gte")
    max_price = django_filters.NumberFilter(field_name="price", lookup_expr="lte")
    min_stock = django_filters.NumberFilter(field_name="stock", lookup_expr="gte")
    max_stock = django_filters.NumberFilter(field_name="stock", lookup_expr="lte")
    product_type = django_filters.ChoiceFilter(choices=Product.ProductType.choices)
    is_active = django_filters.BooleanFilter()
    is_deleted = django_filters.BooleanFilter()
    created_after = django_filters.DateTimeFilter(
        field_name="created_at",
        lookup_expr="gte",
    )
    created_before = django_filters.DateTimeFilter(
        field_name="created_at",
        lookup_expr="lte",
    )

    class Meta:
        model = Product
        fields = (
            "product_type",
            "is_active",
            "is_deleted",
            "min_price",
            "max_price",
            "min_stock",
            "max_stock",
            "created_after",
            "created_before",
        )
