import pytest
from src.test.base import TestBaseClass

@pytest.mark.django_db
class TestUpdateCategoryAPI(TestBaseClass):
    def setup_method(self):
        self.user = self.base_user()
        self.client = self.base_client()
        self.format = self.base_format()
        self.auth = self.authenticate(self.user)

        self.category = self.create_category()
        self.url = f'/uz/api/category/{self.category.id}/'

    def test_successful_put(self):
        payload = {
            "name": "Updated Name"
        }
        response = self.client.put(self.url, payload, format=self.format)
        assert response.status_code == 200
        assert response.data['name'] == "Updated Name"

    def test_invalid_put(self):
        payload = {}
        response = self.client.put(self.url, payload, format=self.format)
        assert response.status_code == 400
        assert 'name' in response.data

    def test_successful_patch(self):
        payload = {
            "name": "Partially Updated Name"
        }
        response = self.client.patch(self.url, payload, format=self.format)
        assert response.status_code == 200
        assert response.data['name'] == "Partially Updated Name"

    def test_invalid_patch(self):
        payload = {
            "name": ""
        }
        response = self.client.patch(self.url, payload, format=self.format)
        assert response.status_code == 400
        assert 'name' in response.data
