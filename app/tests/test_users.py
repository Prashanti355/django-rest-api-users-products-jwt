import pytest


@pytest.mark.django_db
def test_public_user_registration(api_client):
    response = api_client.post(
        "/api/v1/users/",
        {
            "email": "newuser@example.com",
            "username": "newuser",
            "first_name": "New",
            "last_name": "User",
            "password": "NewUser1234",
        },
        format="json",
    )

    assert response.status_code == 201
    assert response.data["email"] == "newuser@example.com"
    assert "password" not in response.data


@pytest.mark.django_db
def test_admin_can_list_users(admin_client, admin_user, customer_user):
    response = admin_client.get("/api/v1/users/")

    assert response.status_code == 200
    assert len(response.data) >= 2


@pytest.mark.django_db
def test_customer_cannot_list_users(customer_client):
    response = customer_client.get("/api/v1/users/")

    assert response.status_code == 403


@pytest.mark.django_db
def test_authenticated_user_can_get_me(customer_client, customer_user):
    response = customer_client.get("/api/v1/users/me/")

    assert response.status_code == 200
    assert response.data["email"] == customer_user.email


@pytest.mark.django_db
def test_admin_can_change_user_role(admin_client, customer_user):
    response = admin_client.patch(
        f"/api/v1/users/{customer_user.id}/set_role/",
        {"role": "STAFF"},
        format="json",
    )

    assert response.status_code == 200
    assert response.data["role"] == "STAFF"

@pytest.mark.django_db
def test_user_can_update_me(customer_client):
    response = customer_client.patch(
        "/api/v1/users/me/",
        {
            "first_name": "Updated",
            "last_name": "Customer",
        },
        format="json",
    )

    assert response.status_code == 200
    assert response.data["first_name"] == "Updated"


@pytest.mark.django_db
def test_admin_can_soft_delete_user(admin_client, customer_user):
    response = admin_client.delete(f"/api/v1/users/{customer_user.id}/")

    assert response.status_code == 204

    customer_user.refresh_from_db()
    assert customer_user.is_deleted is True
    assert customer_user.is_active is False
    assert customer_user.deleted_at is not None


@pytest.mark.django_db
def test_admin_can_restore_deleted_user(admin_client, customer_user):
    customer_user.soft_delete()

    response = admin_client.patch(f"/api/v1/users/{customer_user.id}/restore/")

    assert response.status_code == 200

    customer_user.refresh_from_db()
    assert customer_user.is_deleted is False
    assert customer_user.is_active is True
    assert customer_user.deleted_at is None


@pytest.mark.django_db
def test_customer_cannot_change_user_role(customer_client, customer_user):
    response = customer_client.patch(
        f"/api/v1/users/{customer_user.id}/set_role/",
        {"role": "ADMIN"},
        format="json",
    )

    assert response.status_code == 403


@pytest.mark.django_db
def test_admin_cannot_set_invalid_role(admin_client, customer_user):
    response = admin_client.patch(
        f"/api/v1/users/{customer_user.id}/set_role/",
        {"role": "INVALID"},
        format="json",
    )

    assert response.status_code == 400    