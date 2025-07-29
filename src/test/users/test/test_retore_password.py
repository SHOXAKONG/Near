from django.utils import timezone
from datetime import timedelta
import uuid
from rest_framework.test import APIClient
from src.apps.users.models import Code
import pytest
from src.test.base import TestBaseClass

@pytest.mark.django_db
class TestRestorePasswordAPI(TestBaseClass):
    def setup_method(self):
        self.client = APIClient()
        self.url = '/uz/api/auth/restore_password/'
        self.format = 'json'
        self.user = self.base_user()
        unique_code = str(uuid.uuid4())[:6]
        self.code = Code.objects.create(
            user=self.user,
            code=unique_code,
            expired_time=timezone.now() + timedelta(minutes=10)
        )

    def teardown_method(self):
        try:
            Code.objects.filter(user=self.user).delete()
            self.user.delete()
        except Exception as e:
            print(f"Cleanup error: {e}")
            raise

    def test_successful_restore(self):
        payload = {
            "code": self.code.code,
            "password": "newpassword123",
            "password_confirm": "newpassword123"
        }
        response = self.client.post(self.url, payload, format=self.format)
        assert response.status_code == 200

    def test_invalid_code(self):
        payload = {
            "code": "INVALID",
            "password": "newpassword123",
            "password_confirm": "newpassword123"
        }
        response = self.client.post(self.url, payload, format=self.format)
        assert response.status_code == 400
        assert 'error' in response.data