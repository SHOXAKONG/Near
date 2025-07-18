from django.db import models
from src.apps.category.models import Category
from src.apps.users.models import Users


class SearchHistory(models.Model):
    user = models.ForeignKey(
        Users,
        on_delete=models.CASCADE,
        related_name='search_history'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='search_logs'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Search Timestamp"
    )
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    city = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = "Search History Record"
        verbose_name_plural = "Search History Records"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.email} searched for {self.category.name}"
