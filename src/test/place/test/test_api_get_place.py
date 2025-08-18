import pytest
from src.test.base import TestBaseClass

@pytest.mark.django_db
class TestCreateAPI(TestBaseClass):
    def setup_method(self):
        self.url = '/uz/api/place/'
        self.client = self.base_client()
        self.category = self.create_category()
        self.user = self.base_user()
        self.place = self.create_place(self.user, self.category)
        self.auth = self.authenticate(self.user)
        self.format = self.base_format()

    def test_successful_get_api(self):
        response = self.client.get(self.url, format=self.format)
        assert response.status_code == 200
        assert response.data