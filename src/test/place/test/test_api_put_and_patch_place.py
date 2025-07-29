import json
from io import BytesIO

import pytest
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
from src.test.base import TestBaseClass


@pytest.mark.django_db
class TestUpdatePlaceAPI(TestBaseClass):
    def setup_method(self):
        self.client = self.base_client()
        self.user = self.base_user()
        self.category = self.create_category()
        self.auth = self.authenticate(self.user)
        self.format = self.base_format()
        self.place = self.create_place(user=self.user, category=self.category)

    def generate_test_image(self):
        image = Image.new("RGB", (100, 100), color="red")
        buffer = BytesIO()
        image.save(buffer, format="JPEG")
        return SimpleUploadedFile("test.jpg", buffer.getvalue(), content_type="image/jpeg")

    def test_successful_put_place(self):
        image = self.generate_test_image()
        payload = {
            "name": "Updated Name",
            "description": "Updated Description",
            "category": self.category.id,
            "contact": "Updated Contact",
            "location": {
                "latitude": 41.3300,
                "longitude": 69.2900
            },
            "image": image,
        }

        data = {
            "name": payload["name"],
            "description": payload["description"],
            "category": payload["category"],
            "contact": payload["contact"],
            "location": json.dumps(payload["location"]),
            "image": payload["image"],
        }

        url = f"/uz/api/place/{self.place.id}/"
        response = self.client.put(url, data=data, format="multipart")

        assert response.status_code == 200
        assert response.data["name"] == payload["name"]
        assert response.data["description"] == payload["description"]

    def test_failed_put_place_missing_fields(self):
        url = f"/uz/api/place/{self.place.id}/"
        data = {
            "name": "",
            "description": "",
            "location": json.dumps({"latitude": 0, "longitude": 0}),
        }
        response = self.client.put(url, data=data, format="multipart")

        assert response.status_code == 400
        assert "name" in response.data
        assert "description" in response.data

    def test_successful_patch_place_name_only(self):
        url = f"/uz/api/place/{self.place.id}/"
        payload = {
            "name": "Only Name Patched"
        }

        response = self.client.patch(url, payload, format='multipart')
        print(response.data)

        assert response.status_code == 200
        assert response.data["name"] == payload["name"]

    def test_failed_patch_place_invalid_name(self):
        url = f"/uz/api/place/{self.place.id}/"
        payload = {
            "name": ""
        }

        response = self.client.patch(url, data=payload, format=self.format)

        assert response.status_code == 400
        assert "name" in response.data
