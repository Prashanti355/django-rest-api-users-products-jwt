import pytest

from apps.audit.models import AuditLog
from apps.products.models import Product


@pytest.mark.django_db
def test_login_creates_audit_log(api_client, admin_user):
    response = api_client.post(
        "/api/v1/auth/login/",
        {
            "email": "admin@example.com",
            "password": "Admin1234",
        },
        format="json",
    )

    assert response.status_code == 200
    assert AuditLog.objects.filter(action=AuditLog.Action.LOGIN).exists()


@pytest.mark.django_db
def test_refresh_token_creates_audit_log(api_client, admin_user):
    login_response = api_client.post(
        "/api/v1/auth/login/",
        {
            "email": "admin@example.com",
            "password": "Admin1234",
        },
        format="json",
    )

    refresh_token = login_response.data["refresh"]

    response = api_client.post(
        "/api/v1/auth/refresh/",
        {
            "refresh": refresh_token,
        },
        format="json",
    )

    assert response.status_code == 200
    assert AuditLog.objects.filter(action=AuditLog.Action.TOKEN_REFRESH).exists()


@pytest.mark.django_db
def test_product_create_creates_audit_log(admin_client):
    response = admin_client.post(
        "/api/v1/products/",
        {
            "name": "Producto auditado",
            "description": "Producto para validar auditoría",
            "product_type": Product.ProductType.PHYSICAL,
            "product_key": "AUD001",
            "price": "100.00",
            "stock": 5,
        },
        format="json",
    )

    assert response.status_code == 201
    assert AuditLog.objects.filter(
        action=AuditLog.Action.PRODUCT_CREATE,
        entity_type=AuditLog.EntityType.PRODUCT,
    ).exists()


@pytest.mark.django_db
def test_product_delete_creates_audit_log(admin_client, admin_user):
    product = Product.objects.create(
        name="Producto delete audit",
        description="Producto para auditoría de eliminación",
        product_type=Product.ProductType.PHYSICAL,
        product_key="AUD002",
        price="200.00",
        stock=2,
        owner=admin_user,
    )

    response = admin_client.delete(f"/api/v1/products/{product.id}/")

    assert response.status_code == 204
    assert AuditLog.objects.filter(
        action=AuditLog.Action.PRODUCT_DELETE,
        entity_id=str(product.id),
    ).exists()


@pytest.mark.django_db
def test_user_role_change_creates_audit_log(admin_client, customer_user):
    response = admin_client.patch(
        f"/api/v1/users/{customer_user.id}/set_role/",
        {"role": "STAFF"},
        format="json",
    )

    assert response.status_code == 200
    assert AuditLog.objects.filter(
        action=AuditLog.Action.USER_UPDATE_ROLE,
        entity_id=str(customer_user.id),
    ).exists()


@pytest.mark.django_db
def test_admin_can_list_audit_logs(admin_client):
    AuditLog.objects.create(
        actor_email="admin@example.com",
        action=AuditLog.Action.LOGIN,
        entity_type=AuditLog.EntityType.AUTH,
        detail="Login success for admin@example.com",
    )

    response = admin_client.get("/api/v1/audit-logs/")

    assert response.status_code == 200
    assert len(response.data) >= 1


@pytest.mark.django_db
def test_customer_cannot_list_audit_logs(customer_client):
    response = customer_client.get("/api/v1/audit-logs/")

    assert response.status_code == 403
