from django.db import models
from src.apps.category.models import Category, Subcategory
from src.apps.common.models import BaseModel
from django.contrib.gis.db import models


class Place(BaseModel):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.PROTECT)
    location = models.PointField()
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
