from django.db import models
from src.apps.category.models import Category, Subcategory
from src.apps.common.models import BaseModel


class Place(BaseModel):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.PROTECT)
    latitude = models.CharField(max_length=20)
    longitude = models.CharField(max_length=20)
    contact = models.CharField(max_length=20)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-created_at',)
        db_table = 'place'

