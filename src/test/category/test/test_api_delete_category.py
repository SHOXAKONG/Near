import pytest
from src.test.base import TestBaseClass

@pytest.mark.django_db
class TestDeleteCategoryAPI(TestBaseClass):
    def setup_method(self):
        self.user = self.base_user()
        self.client = self.base_client()
        self.format = self.base_format()
        self.auth = self.authenticate(self.user)
        self.category = self.create_category()
        self.url = f'/uz/api/category/{self.category.id}/'

    def test_successful_delete(self):
        response = self.client.delete(self.url, format=self.format)
        print(response.data)
        assert response.status_code == 204
        assert response.content == b''

    def test_invalid_delete_not_found(self):
        invalid_url = '/uz/api/category/9999/'
        response = self.client.delete(invalid_url, format=self.format)
        assert response.status_code == 404
        assert response.data
