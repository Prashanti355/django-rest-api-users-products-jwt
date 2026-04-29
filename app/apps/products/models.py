import uuid

from django.conf import settings
from django.db import models
from django.utils import timezone


class Product(models.Model):
    class ProductType(models.TextChoices):
        PHYSICAL = "PHYSICAL", "Physical"
        DIGITAL = "DIGITAL", "Digital"
        SERVICE = "SERVICE", "Service"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    product_type = models.CharField(
        max_length=20,
        choices=ProductType.choices,
        default=ProductType.PHYSICAL,
    )

    product_key = models.CharField(max_length=20, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)

    image_link = models.URLField(blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(blank=True, null=True)

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="products",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "products"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["product_key"]),
            models.Index(fields=["is_active", "is_deleted"]),
            models.Index(fields=["created_at"]),
        ]

    def soft_delete(self):
        self.is_deleted = True
        self.is_active = False
        self.deleted_at = timezone.now()
        self.save(update_fields=["is_deleted", "is_active", "deleted_at", "modified_at"])

    def restore(self):
        self.is_deleted = False
        self.is_active = True
        self.deleted_at = None
        self.save(update_fields=["is_deleted", "is_active", "deleted_at", "modified_at"])

    def __str__(self):
        return self.name