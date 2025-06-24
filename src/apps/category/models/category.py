from django.db import models
from src.apps.common.models import BaseModel


class Category(BaseModel):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'category'
