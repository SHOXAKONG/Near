import pytest
from src.test.base import TestBaseClass

@pytest.mark.django_db
class TestRefreshTokenAPI(TestBaseClass):
    def setup_method(self):
        self.url = '/uz/api/auth/login-token/refresh/'
        self.client = self.base_client()
        self.format = self.base_format()

    def test_successful_refresh_token(self):
        payload = {
            "refresh" : f"{self.refresh_token()}"
        }
        response = self.client.post(self.url, payload, self.format)
        # print(response.data)
        assert response.status_code == 200
        assert "access" in response.data

    def test_invalid_refresh_token(self):
        payload = {
            "refresh": "non_field"
        }
        response = self.client.post(self.url, payload, self.format)
        assert response.status_code == 401
        assert "detail" in response.data
