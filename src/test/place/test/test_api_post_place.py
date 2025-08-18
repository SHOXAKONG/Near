import json

import pytest
from io import BytesIO

from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
# from django.contrib.gis.geos import Point
from src.test.base import TestBaseClass


@pytest.mark.django_db
class TestPostAPI(TestBaseClass):
    def setup_method(self):
        self.url = '/uz/api/place/'
        self.client = self.base_client()
        self.user = self.base_user()
        self.category = self.create_category()
        self.auth = self.authenticate(self.user)
        self.format = self.base_format()

    def generate_test_image(self):
        image = Image.new("RGB", (100, 100), color="red")
        buffer = BytesIO()
        image.save(buffer, format="JPEG")
        return SimpleUploadedFile(
            "test.jpg",
            buffer.getvalue(),
            content_type="image/jpeg"
        )

    def test_successful_post_api(self):
        image = self.generate_test_image()

        payload = {
            "name": "Test Place",
            "description": "Test description",
            "category": self.category.id,
            "contact": "Test contact info",
            "location": {
                "latitude": 41.3111,
                "longitude": 69.2797
            }
        }

        data = {
            "name": payload["name"],
            "description": payload["description"],
            "category": payload["category"],
            "contact": payload["contact"],
            "location": json.dumps(payload["location"]),
            "image": image,
        }

        response = self.client.post(
            self.url,
            data=data,
            format='multipart',
            # **(self.auth or {})
        )

        assert response.status_code == 201, response.data
        assert response.data["name"] == payload["name"]

    def test_invalid_location_string(self):
        image = self.generate_test_image()

        payload = {
            "name": "Test Place",
            "description": "Test description",
            "category": self.category.id,
            "contact": "Test contact info",
            "location": "POINT(69.2797 41.3111)",
            "image": image,
        }

        response = self.client.post(
            self.url,
            data=payload,
            format='multipart',
            **(self.auth or {})
        )

        assert response.status_code == 400
        assert "location" in response.data
        assert response.data["location"][0] == "Location string is not valid JSON."


    def test_empty_location(self):
        image = self.generate_test_image()

        payload = {
            "name": "Test Place",
            "description": "Test description",
            "category": self.category.id,
            "contact": "Test contact info",
            "location": "",
            "image": image,
        }

        response = self.client.post(
            self.url,
            data=payload,
            format='multipart',
            **(self.auth or {})
        )

        assert response.status_code == 400
        assert "location" in response.data


