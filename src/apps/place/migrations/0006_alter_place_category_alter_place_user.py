# Generated by Django 5.2.3 on 2025-07-11 13:07

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0002_delete_subcategory'),
        ('place', '0005_place_user'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='place',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='place_category', to='category.category'),
        ),
        migrations.AlterField(
            model_name='place',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='place_user', to=settings.AUTH_USER_MODEL),
        ),
    ]
