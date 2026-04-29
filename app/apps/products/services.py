from django.db import transaction

from apps.products.models import Product


@transaction.atomic
def create_product(validated_data):
    return Product.objects.create(**validated_data)


@transaction.atomic
def update_product(product, validated_data):
    for field, value in validated_data.items():
        setattr(product, field, value)

    product.save()
    return product


@transaction.atomic
def soft_delete_product(product):
    product.soft_delete()
    return product


@transaction.atomic
def restore_product(product):
    product.restore()
    return product