import pytest
from src.test.base import TestBaseClass


@pytest.mark.django_db
class TestBecomeAPI(TestBaseClass):
    def setup_method(self):
        self.url = '/uz/api/auth/become-entrepreneur/'
        self.user = self.base_user()
        self.format = self.base_format()
        self.client = self.base_client()
        self.auth = self.authenticate(self.user)

    def test_successful_become(self):
        payload = {}
        response = self.client.post(self.url, payload, self.format)
        assert response.status_code == 200
        assert 'message' in response.data

    def test_invalid_become(self):
        self.user.role = 'admin'
        self.user.save()
        payload = {}
        response = self.client.post(self.url, payload, self.format)
        assert response.status_code == 403
        assert 'detail' in response.data
