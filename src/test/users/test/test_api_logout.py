import pytest
from rest_framework_simplejwt.tokens import RefreshToken

from src.test.base import TestBaseClass


@pytest.mark.django_db
class TestLogoutAPI(TestBaseClass):
    def setup_method(self):
        self.client = self.base_client()
        self.format = self.base_format()
        self.user = self.base_user()
        self.url = '/uz/api/auth/logout/'
        self.refresh = RefreshToken.for_user(self.user)
        self.access_token = str(self.refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")

    def test_successful_logout(self):
        response = self.client.delete(self.url, format=self.format)
        assert response.status_code == 200
        assert 'message' in response.data

    def test_logout_without_auth(self):
        self.client.credentials()
        response = self.client.delete(self.url, format=self.format)

        assert response.status_code == 401
        assert "detail" in response.data
