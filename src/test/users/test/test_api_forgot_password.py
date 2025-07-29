import pytest
from rest_framework.test import APIClient
from src.apps.users.models import Users

@pytest.mark.django_db
class TestForgotPasswordAPI:
    def setup_method(self):
        self.client = APIClient()
        Users.objects.create_user(email='test@info.com', password='1234Test')
        self.url = '/uz/api/auth/forgot_password/'
        self.format = 'json'


    def test_api_successfully(self):

        payload = {
            "email" : "test@info.com"
        }
        response = self.client.post(self.url, payload, self.format)
        assert response.status_code == 200
        assert 'message' in response.data

    def test_api_invalid_email(self):

        payload = {
            "email" : "non_email"
        }
        response = self.client.post(self.url, payload, self.format)
        assert response.status_code == 400
        assert 'email' in response.data

    def test_api_existing_email(self):
        payload = {
            "email" : "test1@info.com"
        }

        response = self.client.post(self.url, payload, self.format)
        assert response.status_code == 400
        assert 'email' in response.data