import pytest
from src.test.base import TestBaseClass

@pytest.mark.django_db
class TestPostAPI(TestBaseClass):
    def setup_method(self):
        self.user = self.base_user()
        self.url = '/uz/api/category/'
        self.client = self.base_client()
        self.format = self.base_format()
        self.auth = self.authenticate(self.user)

    def test_successful_post(self):
        payload = {
            "name" : "Test"
        }

        response = self.client.post(self.url, payload, format=self.format)
        assert response.status_code == 201
        assert response.data

    def test_invalid_post(self):
        payload = {
            # "name" : "Test"
        }

        response = self.client.post(self.url, payload, format=self.format)
        assert response.status_code == 400
        assert response.data