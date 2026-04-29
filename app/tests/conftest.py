import pytest
from rest_framework.test import APIClient

from apps.users.models import User


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def admin_user(db):
    return User.objects.create_user(
        email="admin@example.com",
        username="admin",
        password="Admin1234",
        first_name="Admin",
        last_name="User",
        role=User.Role.ADMIN,
        is_staff=True,
        is_superuser=True,
    )


@pytest.fixture
def staff_user(db):
    return User.objects.create_user(
        email="staff@example.com",
        username="staff",
        password="Staff1234",
        first_name="Staff",
        last_name="User",
        role=User.Role.STAFF,
        is_staff=True,
    )


@pytest.fixture
def customer_user(db):
    return User.objects.create_user(
        email="customer@example.com",
        username="customer",
        password="Customer1234",
        first_name="Customer",
        last_name="User",
        role=User.Role.CUSTOMER,
    )


@pytest.fixture
def admin_client(api_client, admin_user):
    api_client.force_authenticate(user=admin_user)
    return api_client


@pytest.fixture
def staff_client(api_client, staff_user):
    api_client.force_authenticate(user=staff_user)
    return api_client


@pytest.fixture
def customer_client(api_client, customer_user):
    api_client.force_authenticate(user=customer_user)
    return api_client
