import logging


class DatabaseHandler(logging.Handler):
    def emit(self, record):
        try:
            from src.apps.logs.models.log_entry import LogEntry

            LogEntry.objects.create(level=record.levelname, message=self.format(record))
        except Exception:
            pass
