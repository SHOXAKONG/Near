from .settings import *

DEBUG = True

# Faster hashing & no validators
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]
AUTH_PASSWORD_VALIDATORS = []

# In-memory services
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
CACHES = {"default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"}}

# Avoid network I/O in tests
DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"

# If you use Celery
CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True
