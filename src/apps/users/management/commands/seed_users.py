import random
from django.core.management.base import BaseCommand
from django.db import transaction
from faker import Faker
from django.contrib.auth.hashers import make_password

from src.apps.users.models import Users


class Command(BaseCommand):
    help = 'Seeds the database with fake users using bulk_create for efficiency.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--number',
            type=int,
            help='The number of fake users to create.',
            default=12000
        )

    @transaction.atomic
    def handle(self, *args, **options):
        number = options['number']
        fake = Faker()

        self.stdout.write('Starting user creation process...')

        self.stdout.write('Fetching existing emails...')
        existing_emails = set(Users.objects.values_list('email', flat=True))
        self.stdout.write(f'Found {len(existing_emails)} existing emails.')

        new_emails = set()
        self.stdout.write(f'Generating {number} unique new emails...')

        while len(new_emails) < number:
            email = fake.email()
            if email not in existing_emails and email not in new_emails:
                new_emails.add(email)

            if len(new_emails) % 100 == 0:
                pass

        self.stdout.write('Preparing user objects for creation...')
        users_to_create = []
        hashed_password = make_password('1234Shbn')

        for email in new_emails:
            user = Users(
                email=email,
                password=hashed_password,
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                age=random.randint(18, 70),
            )
            users_to_create.append(user)

        self.stdout.write(f'Creating {len(users_to_create)} new users in a single transaction...')
        Users.objects.bulk_create(users_to_create)

        self.stdout.write(self.style.SUCCESS(f'Successfully created {number} users.'))
