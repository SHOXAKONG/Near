import pytest
from src.test.base import TestBaseClass

@pytest.mark.django_db
class TestGetCategoryAPI(TestBaseClass):
    def setup_method(self):
        self.user = self.base_user()
        self.url = '/uz/api/category/'
        self.client = self.base_client()
        self.format = self.base_format()
        self.auth = self.authenticate(self.user)
        self.category = self.create_category()

    def test_get_category_list(self):
        response = self.client.get(self.url, format=self.format)
        assert response.status_code == 200
        assert isinstance(response.data, list) or "results" in response.data
        assert len(response.data) >= 2

    def test_get_category_detail(self):
        detail_url = f"{self.url}{self.category.id}/"

        response = self.client.get(detail_url, format=self.format)
        assert response.status_code == 200
        assert response.data["id"] == self.category.id
        assert response.data["name"] == self.category.name

    def test_get_nonexistent_category_detail(self):
        invalid_url = f"{self.url}999999/"

        response = self.client.get(invalid_url, format=self.format)
        assert response.status_code == 404
