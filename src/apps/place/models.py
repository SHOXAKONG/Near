from PIL import Image
from src.apps.category.models import Category
from src.apps.common.models import BaseModel
from django.contrib.gis.db import models

from src.apps.users.models import Users


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

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image and hasattr(obj.image, 'url'):
            return request.build_absolute_uri(obj.image.url)
        return None

    class Meta:
        ordering = ('-created_at',)
        db_table = 'place'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img_path = self.image.path

        img = Image.open(img_path)

        width, height = img.size
        min_dim = min(width, height)
        left = (width - min_dim) / 2
        top = (height - min_dim) / 2
        right = (width + min_dim) / 2
        bottom = (height + min_dim) / 2
        img = img.crop((left, top, right, bottom))

        try:
            resample_method = Image.Resampling.LANCZOS
        except AttributeError:
            resample_method = Image.ANTIALIAS

        img = img.resize((300, 300), resample_method)

        img.save(img_path, optimize=True, quality=85)
