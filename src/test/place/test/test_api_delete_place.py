import pytest
from src.test.base import TestBaseClass

@pytest.mark.django_db
class TestPostAPI(TestBaseClass):
    def setup_method(self):
        self.client = self.base_client()
        self.user = self.base_user()
        self.category = self.create_category()
        self.auth = self.authenticate(self.user)
        self.format = self.base_format()

    def test_delete_success_place(self):
        place = self.create_place(user=self.user, category=self.category)

        url = f'/uz/api/place/{place.id}/'

        response = self.client.delete(url, format=self.format)

        assert response.status_code in [204, 200, 202], response.data
