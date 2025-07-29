from django.utils import timezone
from datetime import timedelta
import uuid
from src.apps.users.models import Code
from src.test.base import TestBaseClass
import pytest

@pytest.mark.django_db
class TestConfirmAPI(TestBaseClass):
    def setup_method(self):
        self.client = self.base_client()
        self.url = '/uz/api/auth/confirm/'
        self.format = self.base_format()
        self.user = self.base_user(email=f'test_{uuid.uuid4().hex[:6]}@info.com')
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
            print(f"Error in teardown: {e}")
            raise

    def test_successful_confirm(self):
        payload = {
            "code": self.code.code
        }
        response = self.client.post(self.url, payload, format=self.format)
        assert response.status_code == 200
        assert "refresh" in response.data
        assert "access" in response.data

    def test_invalid_code(self):
        payload = {
            "code": "INVALID"
        }
        response = self.client.post(self.url, payload, format=self.format)
        assert response.status_code == 400
        assert 'code' in response.data