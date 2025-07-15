import random
from django.core.management.base import BaseCommand
from django.db import transaction

from src.apps.users.models import Users
from src.apps.category.models import Category
from src.apps.history.models import SearchHistory


class Command(BaseCommand):
    help = 'Seeds the database with fake search history records'

    def add_arguments(self, parser):
        parser.add_argument(
            '--number',
            type=int,
            help='The number of fake search history records to create.',
            default=1000
        )

    @transaction.atomic
    def handle(self, *args, **options):
        number_of_records = options['number']
        self.stdout.write(f'Preparing to create {number_of_records} search history records...')

        users = list(Users.objects.all())
        categories = list(Category.objects.all())

        if not users or not categories:
            self.stdout.write(self.style.ERROR(
                'Error: You must have users and categories in your database to create a search history.'
            ))
            self.stdout.write(self.style.NOTICE(
                'Please run `python manage.py seed_users` and ensure you have categories.'
            ))
            return

        self.stdout.write('Creating search history records...')

        history_to_create = []
        for i in range(number_of_records):
            random_user = random.choice(users)
            random_category = random.choice(categories)
            history_to_create.append(
                SearchHistory(user=random_user, category=random_category)
            )

            if (i + 1) % 500 == 0:
                self.stdout.write(f'  {i + 1}/{number_of_records} records prepared...')

        SearchHistory.objects.bulk_create(history_to_create)

        self.stdout.write(self.style.SUCCESS(
            f'Successfully created {number_of_records} search history records.'
        ))