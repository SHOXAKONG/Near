from django.db import models
from src.apps.category.models.category import Category
from src.apps.common.models import BaseModel


class Subcategory(BaseModel):
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'subcategory'