import pytest

from src.test.base import TestBaseClass

@pytest.mark.django_db
class TestUsersAPI(TestBaseClass):
    def setup_method(self):
        self.url = '/uz/api/auth/users/'
        self.client = self.base_client()
        self.format = self.base_format()
        self.user = self.base_user()
        self.auth = self.authenticate(self.user)

    def test_successful(self):
        response = self.client.get(self.url, format=self.format)
        assert response.status_code == 200
        assert response.data

    def test_successful_users_id(self):
        user_id = self.user.id
        self.url = f'/uz/api/auth/users-data/{user_id}/'
        response = self.client.get(self.url, format=self.format)
        assert response.status_code == 200
        assert response.data
