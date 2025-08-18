import io
import os
import uuid
from unicodedata import category

from PIL import Image
from django.contrib.gis.geos import Point
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from src.apps.category.models import Category
from src.apps.place.models import Place
from src.apps.users.models import Users
from src.apps.history.models import SearchHistory


class TestBaseClass:
    def base_client(self):
        return APIClient()

    def base_format(self):
        return 'json'

    def base_user(self, email=None):
        email = email or f'test_{uuid.uuid4().hex[:6]}@info.com'
        return Users.objects.create_user(email=email, password='password123')

    def refresh_token(self):
        self.refresh = RefreshToken.for_user(self.base_user())
        return str(self.refresh)

    def authenticate(self, user):
        self.refresh = RefreshToken.for_user(user)
        self.access_token = str(self.refresh.access_token)
        self.client = self.base_client()
        return self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")

    def create_category(self):
        return Category.objects.create(name='Test Category')

    def create_place(self, user, category):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        image_path = os.path.join(base_dir, 'media', 'place_images', 'test.png')

        with open(image_path, 'rb') as f:
            image = Image.open(f).convert('RGB')
            buffer = io.BytesIO()
            image.save(buffer, format='JPEG')
            buffer.seek(0)

            test_image = SimpleUploadedFile(
                name='test.jpg',
                content=buffer.read(),
                content_type='image/jpeg'
            )

        return Place.objects.create(
            name="Test",
            user=user,
            category=category,
            location=Point(69.2797, 41.3111),
            description="Test Description",
            image=test_image,
            contact='Test Contact'
        )

    def create_search_history(self, user, category):
        return SearchHistory.objects.create(
            user=user,
            category=category,
            latitude=41.3111,
            longitude=69.2797,
        )
