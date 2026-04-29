import pytest

from apps.products.models import Product


@pytest.fixture
def product(admin_user):
    return Product.objects.create(
        name="Laptop",
        description="Laptop de prueba",
        product_type=Product.ProductType.PHYSICAL,
        product_key="LAP001",
        price="12000.00",
        stock=5,
        owner=admin_user,
        is_active=True,
    )


@pytest.mark.django_db
def test_admin_can_create_product(admin_client):
    response = admin_client.post(
        "/api/v1/products/",
        {
            "name": "Mouse",
            "description": "Mouse inalámbrico",
            "product_type": "PHYSICAL",
            "product_key": "MOU001",
            "price": "500.00",
            "stock": 10,
        },
        format="json",
    )

    assert response.status_code == 201
    assert response.data["name"] == "Mouse"


@pytest.mark.django_db
def test_staff_can_create_product(staff_client):
    response = staff_client.post(
        "/api/v1/products/",
        {
            "name": "Keyboard",
            "description": "Teclado mecánico",
            "product_type": "PHYSICAL",
            "product_key": "KEY001",
            "price": "1500.00",
            "stock": 3,
        },
        format="json",
    )

    assert response.status_code == 201


@pytest.mark.django_db
def test_customer_cannot_create_product(customer_client):
    response = customer_client.post(
        "/api/v1/products/",
        {
            "name": "Monitor",
            "description": "Monitor 24 pulgadas",
            "product_type": "PHYSICAL",
            "product_key": "MON001",
            "price": "3000.00",
            "stock": 2,
        },
        format="json",
    )

    assert response.status_code == 403


@pytest.mark.django_db
def test_authenticated_user_can_list_products(customer_client, product):
    response = customer_client.get("/api/v1/products/")

    assert response.status_code == 200
    assert len(response.data) >= 1


@pytest.mark.django_db
def test_admin_can_soft_delete_product(admin_client, product):
    response = admin_client.delete(f"/api/v1/products/{product.id}/")

    assert response.status_code == 204

    product.refresh_from_db()
    assert product.is_deleted is True
    assert product.is_active is False


@pytest.mark.django_db
def test_customer_cannot_delete_product(customer_client, product):
    response = customer_client.delete(f"/api/v1/products/{product.id}/")

    assert response.status_code == 403


@pytest.mark.django_db
def test_search_products(admin_client, product):
    response = admin_client.get("/api/v1/products/search/?q=Laptop")

    assert response.status_code == 200
    assert len(response.data) >= 1


@pytest.mark.django_db
def test_filter_products_by_price(admin_client, product):
    response = admin_client.get(
        "/api/v1/products/by_price/?min_price=10000&max_price=13000"
    )

    assert response.status_code == 200
    assert len(response.data) >= 1


@pytest.mark.django_db
def test_staff_can_update_product(staff_client, product):
    response = staff_client.patch(
        f"/api/v1/products/{product.id}/",
        {
            "name": "Laptop actualizada",
            "price": "11500.00",
        },
        format="json",
    )

    assert response.status_code == 200

    product.refresh_from_db()
    assert product.name == "Laptop actualizada"
    assert str(product.price) == "11500.00"


@pytest.mark.django_db
def test_admin_can_restore_deleted_product(admin_client, product):
    product.soft_delete()

    response = admin_client.patch(f"/api/v1/products/{product.id}/restore/")

    assert response.status_code == 200

    product.refresh_from_db()
    assert product.is_deleted is False
    assert product.is_active is True
    assert product.deleted_at is None


@pytest.mark.django_db
def test_customer_can_only_see_active_products(customer_client, admin_user):
    Product.objects.create(
        name="Producto activo",
        description="Visible",
        product_type=Product.ProductType.PHYSICAL,
        product_key="ACT001",
        price="100.00",
        stock=1,
        owner=admin_user,
        is_active=True,
    )

    Product.objects.create(
        name="Producto inactivo",
        description="No visible",
        product_type=Product.ProductType.PHYSICAL,
        product_key="INA001",
        price="100.00",
        stock=1,
        owner=admin_user,
        is_active=False,
    )

    response = customer_client.get("/api/v1/products/")

    assert response.status_code == 200
    product_names = [item["name"] for item in response.data]

    assert "Producto activo" in product_names
    assert "Producto inactivo" not in product_names


@pytest.mark.django_db
def test_product_creation_fails_with_negative_price(admin_client):
    response = admin_client.post(
        "/api/v1/products/",
        {
            "name": "Producto inválido",
            "description": "Precio negativo",
            "product_type": "PHYSICAL",
            "product_key": "NEG001",
            "price": "-10.00",
            "stock": 1,
        },
        format="json",
    )

    assert response.status_code == 400
    assert "price" in response.data


@pytest.mark.django_db
def test_product_creation_fails_with_negative_stock(admin_client):
    response = admin_client.post(
        "/api/v1/products/",
        {
            "name": "Producto inválido",
            "description": "Stock negativo",
            "product_type": "PHYSICAL",
            "product_key": "NST001",
            "price": "10.00",
            "stock": -1,
        },
        format="json",
    )

    assert response.status_code == 400
    assert "stock" in response.data


@pytest.mark.django_db
def test_search_products_without_results(admin_client):
    response = admin_client.get("/api/v1/products/search/?q=noexiste")

    assert response.status_code == 200
    assert len(response.data) == 0
