from django.db import transaction

from apps.audit.models import AuditLog
from apps.audit.services import create_audit_log
from apps.products.models import Product


@transaction.atomic
def create_product(validated_data, actor=None, request=None):
    product = Product.objects.create(**validated_data)

    create_audit_log(
        action=AuditLog.Action.PRODUCT_CREATE,
        entity_type=AuditLog.EntityType.PRODUCT,
        entity_id=product.id,
        actor=actor,
        detail=f"Product created: {product.name}",
        request=request,
    )

    return product


@transaction.atomic
def update_product(product, validated_data, actor=None, request=None):
    for field, value in validated_data.items():
        setattr(product, field, value)

    product.save()

    create_audit_log(
        action=AuditLog.Action.PRODUCT_UPDATE,
        entity_type=AuditLog.EntityType.PRODUCT,
        entity_id=product.id,
        actor=actor,
        detail=f"Product updated: {product.name}",
        request=request,
    )

    return product


@transaction.atomic
def soft_delete_product(product, actor=None, request=None):
    product.soft_delete()

    create_audit_log(
        action=AuditLog.Action.PRODUCT_DELETE,
        entity_type=AuditLog.EntityType.PRODUCT,
        entity_id=product.id,
        actor=actor,
        detail=f"Product soft deleted: {product.name}",
        request=request,
    )

    return product


@transaction.atomic
def restore_product(product, actor=None, request=None):
    product.restore()

    create_audit_log(
        action=AuditLog.Action.PRODUCT_RESTORE,
        entity_type=AuditLog.EntityType.PRODUCT,
        entity_id=product.id,
        actor=actor,
        detail=f"Product restored: {product.name}",
        request=request,
    )

    return product