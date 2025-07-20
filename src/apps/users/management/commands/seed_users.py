import random
from django.core.management.base import BaseCommand
from django.db import transaction
from faker import Faker

from src.apps.users.models import Users

class Command(BaseCommand):
    help = 'Seeds the database with fake users, ensuring email uniqueness.'

    def add_arguments(self, parser):
        parser.add_argument('--number', type=int, help='The number of fake users to create.', default=1200)

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write('Starting to create new users...')
        number = options['number']
        fake = Faker()

        self.stdout.write(f'Creating {number} new users...')

        for i in range(number):
            while True:
                email = fake.email()
                if not Users.objects.filter(email=email).exists():
                    break

            first_name = fake.first_name()
            last_name = fake.last_name()
            age = random.randint(18, 70)

            Users.objects.create_user(
                email=email,
                password='1234Shbn',
                first_name=first_name,
                last_name=last_name,
                age=age,
            )

            if (i + 1) % 100 == 0:
                self.stdout.write(f'  {i + 1}/{number} users created...')

        self.stdout.write(self.style.SUCCESS(f'Successfully created {number} users.'))
