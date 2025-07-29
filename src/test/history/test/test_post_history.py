import pytest
from src.test.base import TestBaseClass


@pytest.mark.django_db
class TestPostAPI(TestBaseClass):
    def setup_method(self):
        self.user = self.base_user()
        self.url = '/uz/api/search-history/'
        self.client = self.base_client()
        self.format = self.base_format()
        self.auth = self.authenticate(self.user)
        self.category = self.create_category()

    def test_successful_post(self):
        payload = {
            "category": self.category.id,
            "latitude": "44.97425",
            "longitude": "-29.45811"
        }

        response = self.client.post(self.url, payload, format=self.format)
        assert response.status_code == 201
        assert response.data

    def test_invalid_post(self):
        payload = {
            # Missing required fields
            # "category": self.category.id,
            # "latitude": "44.97425",
            # "longitude": "-29.45811"
        }

        response = self.client.post(self.url, payload, format=self.format)

        assert response.status_code == 400
        assert "category" in response.data or "latitude" in response.data or "longitude" in response.data
