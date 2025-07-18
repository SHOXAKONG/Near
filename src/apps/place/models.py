import os
from io import BytesIO
from django.core.files.base import ContentFile
from PIL import Image
from src.apps.category.models import Category
from src.apps.common.models import BaseModel
from django.contrib.gis.db import models
from src.apps.users.models import Users
from src.api.place.utils import add_watermark


class Place(BaseModel):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='place_user')
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='place_category')
    location = models.PointField()
    description = models.TextField()
    image = models.ImageField(upload_to='place_images/')
    contact = models.CharField(max_length=20)

    @property
    def geomap_longitude(self):
        return self.location.x if self.location else None

    @property
    def geomap_latitude(self):
        return self.location.y if self.location else None

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-created_at',)
        db_table = 'place'

    def save(self, *args, **kwargs):
        if self.image and hasattr(self.image, 'file'):
            in_mem_file = BytesIO(self.image.read())
            img = Image.open(in_mem_file)

            width, height = img.size
            min_dim = min(width, height)
            left = (width - min_dim) / 2
            top = (height - min_dim) / 2
            right = (width + min_dim) / 2
            bottom = (height + min_dim) / 2
            img = img.crop((left, top, right, bottom))
            resample_method = Image.Resampling.LANCZOS
            img = img.resize((300, 300), resample_method)

            temp_buffer = BytesIO()
            img.save(temp_buffer, format='JPEG', quality=85, optimize=True)
            image_bytes = temp_buffer.getvalue()

            watermarked_bytes = add_watermark(image_bytes)

            img_name = os.path.splitext(self.image.name)[0] + '.png'
            self.image = ContentFile(watermarked_bytes, name=img_name)

        super().save(*args, **kwargs)