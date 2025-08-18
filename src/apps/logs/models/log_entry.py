from django.db import models


class LogEntry(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    level = models.CharField(max_length=20)
    logger_name = models.CharField(max_length=255)
    message = models.TextField()

    def __str__(self):
        return f"[{self.level}] {self.logger_name}: {self.message}"
