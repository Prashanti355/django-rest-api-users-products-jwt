import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        STAFF = "STAFF", "Staff"
        CUSTOMER = "CUSTOMER", "Customer"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    email = models.EmailField(unique=True)

    profile_picture = models.URLField(blank=True, null=True)

    email_verified = models.BooleanField(default=False)
    email_verified_at = models.DateTimeField(blank=True, null=True)

    nationality = models.CharField(max_length=50, blank=True, null=True)
    occupation = models.CharField(max_length=80, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    contact_phone_number = models.CharField(max_length=20, blank=True, null=True)

    gender = models.CharField(max_length=30, blank=True, null=True)

    address = models.TextField(blank=True, null=True)
    address_number = models.CharField(max_length=25, blank=True, null=True)
    address_interior_number = models.CharField(max_length=25, blank=True, null=True)
    address_complement = models.TextField(blank=True, null=True)
    address_neighborhood = models.CharField(max_length=100, blank=True, null=True)
    address_zip_code = models.CharField(max_length=10, blank=True, null=True)
    address_city = models.CharField(max_length=100, blank=True, null=True)
    address_state = models.CharField(max_length=100, blank=True, null=True)

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.CUSTOMER,
    )

    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    class Meta:
        db_table = "users"
        ordering = ["-created_at"]

    def soft_delete(self):
        self.is_deleted = True
        self.is_active = False
        self.deleted_at = timezone.now()
        self.save(
            update_fields=["is_deleted", "is_active", "deleted_at", "modified_at"]
        )

    def restore(self):
        self.is_deleted = False
        self.is_active = True
        self.deleted_at = None
        self.save(
            update_fields=["is_deleted", "is_active", "deleted_at", "modified_at"]
        )

    def verify_email(self):
        self.email_verified = True
        self.email_verified_at = timezone.now()
        self.save(update_fields=["email_verified", "email_verified_at", "modified_at"])

    def __str__(self):
        return self.email
