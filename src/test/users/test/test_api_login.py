import pytest
from rest_framework.test import APIClient
from src.apps.users.models import Users


@pytest.mark.django_db
def test_login_success():
    Users.objects.create_user(
        email='test@info.com',
        password='Test1234'
    )

    client = APIClient()
    payload = {
        "email": "test@info.com",
        "password": "Test1234"
    }

    response = client.post('/uz/api/auth/login/', payload, format='json')

    assert response.status_code == 200
    assert "access" in response.data
    assert "refresh" in response.data


@pytest.mark.django_db
def test_invalid_login_password():
    Users.objects.create_user(
        email='test@info.com',
        password='Test1234'
    )

    client = APIClient()
    payload = {
        "email": "test@info.com",
        "password": "Test12345"
    }
    response = client.post('/uz/api/auth/login/', payload, format='json')

    assert response.status_code == 401 or response.status_code == 400
    assert "non_field_errors" in response.data or 'detail' in response.data


@pytest.mark.django_db
def test_login_nonexists_user():
    client = APIClient()
    payload = {
        "email": "test@info.com",
        "password": "Test12345"
    }
    response = client.post('/uz/api/auth/login/', payload, format='json')

    assert response.status_code == 401 or response.status_code == 400
    assert "non_field_errors" in response.data or 'detail' in response.data
