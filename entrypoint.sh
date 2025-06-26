#!/bin/bash
set -e

echo "Running Migrations"
python manage.py migrate

echo "Checking for superuser..."
python manage.py shell <<EOF
from decouple import config
from django.contrib.auth import get_user_model
from django.core.exceptions import ImproperlyConfigured

User = get_user_model()

email = config('DJANGO_SUPERUSER_EMAIL', default='admin@info.com')

try:
    password = config('DJANGO_SUPERUSER_PASSWORD')
except ImproperlyConfigured:
    password = None

# Check for user existence using the email field.
if not User.objects.filter(email=email).exists():
    if not password:
        print("DJANGO_SUPERUSER_PASSWORD not found in environment or .env file. Cannot create superuser.")
        exit(1)

    print(f"Creating superuser for email '{email}'")
    User.objects.create_superuser(email=email, password=password)
    print("Superuser created successfully.")
else:
    print(f"Superuser with email '{email}' already exists. Skipping.")
EOF

echo "Collecting static files"
python manage.py collectstatic --noinput

exec "$@"