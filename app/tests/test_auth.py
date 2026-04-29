import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_login_returns_access_and_refresh_tokens(api_client, admin_user):
    url = reverse("token_obtain_pair")

    response = api_client.post(
        url,
        {
            "email": "admin@example.com",
            "password": "Admin1234",
        },
        format="json",
    )

    assert response.status_code == 200
    assert "access" in response.data
    assert "refresh" in response.data


@pytest.mark.django_db
def test_login_fails_with_invalid_password(api_client, admin_user):
    url = reverse("token_obtain_pair")

    response = api_client.post(
        url,
        {
            "email": "admin@example.com",
            "password": "wrong-password",
        },
        format="json",
    )

    assert response.status_code == 401


@pytest.mark.django_db
def test_refresh_token_returns_new_access_token(api_client, admin_user):
    login_url = reverse("token_obtain_pair")
    refresh_url = reverse("token_refresh")

    login_response = api_client.post(
        login_url,
        {
            "email": "admin@example.com",
            "password": "Admin1234",
        },
        format="json",
    )

    refresh_token = login_response.data["refresh"]

    response = api_client.post(
        refresh_url,
        {
            "refresh": refresh_token,
        },
        format="json",
    )

    assert response.status_code == 200
    assert "access" in response.data