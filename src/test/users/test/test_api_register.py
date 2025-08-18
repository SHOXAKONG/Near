import pytest
from src.apps.users.models import Users
from rest_framework.test import APIClient

@pytest.mark.django_db
class TestRegisterAPI:
    def setup_method(self):
        self.client = APIClient()

    def test_register_successfully(self):
        payload = {
            "first_name": "test_name",
            "last_name": "test_name",
            "email": "test@info.com",
            "password": "1234Something",
            "password_confirm": "1234Something"
        }

        response = self.client.post('/uz/api/auth/register/', payload, format='json')
        # print(response.data)

        assert response.status_code == 201
        assert 'message' in response.data
        assert Users.objects.filter(email='test@info.com').exists()


    def test_user_existing(self):

        Users.objects.create_user(email='test@info.com', password='1234Something')

        payload = {
            "first_name": "test_name",
            "last_name": "test_name",
            "email": "test@info.com",
            "password": "1234Something",
            "password_confirm": "1234Something"
        }

        response = self.client.post('/uz/api/auth/register/', payload, format='json')

        assert response.status_code == 400
        assert 'email' in response.data


    def test_user_invalid_email(self):
        payload = {
            "first_name": "test_name",
            "last_name": "test_name",
            "email": "email",
            "password": "1234Something",
            "password_confirm": "1234Something"
        }
        response = self.client.post('/uz/api/auth/register/', payload, format='json')
        assert response.status_code == 400
        assert 'email' in response.data



    def test_user_invalid_password(self):
        payload = {
            "first_name": "test_name",
            "last_name": "test_name",
            "email": "admin@info.com",
            "password": "1234",
            "password_confirm": "1234"
        }
        response = self.client.post('/uz/api/auth/register/', payload, format='json')
        assert response.status_code == 400
        assert 'non_field_errors' in response.data