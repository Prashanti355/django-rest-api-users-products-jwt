from rest_framework import serializers

from apps.products.models import Product


class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "description",
            "product_type",
            "product_key",
            "price",
            "stock",
            "image_link",
        )

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("El precio no puede ser negativo.")
        return value

    def validate_stock(self, value):
        if value < 0:
            raise serializers.ValidationError("El stock no puede ser negativo.")
        return value

    def create(self, validated_data):
        request = self.context["request"]
        validated_data["owner"] = request.user
        return super().create(validated_data)


class ProductListSerializer(serializers.ModelSerializer):
    owner_email = serializers.EmailField(source="owner.email", read_only=True)

    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "product_type",
            "price",
            "stock",
            "is_active",
            "owner_email",
        )


class ProductDetailSerializer(serializers.ModelSerializer):
    owner_email = serializers.EmailField(source="owner.email", read_only=True)

    class Meta:
        model = Product
        exclude = ()


class ProductUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = (
            "id",
            "owner",
            "created_at",
            "modified_at",
            "deleted_at",
        )

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("El precio no puede ser negativo.")
        return value
