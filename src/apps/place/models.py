from django.db import models
from src.apps.category.models import Category
from src.apps.common.models import BaseModel
from django.contrib.gis.db import models

from src.apps.users.models import Users


class Place(BaseModel):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
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
