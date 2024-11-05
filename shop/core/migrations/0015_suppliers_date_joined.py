# Generated by Django 5.1.2 on 2024-11-05 19:12

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_suppliers'),
    ]

    operations = [
        migrations.AddField(
            model_name='suppliers',
            name='date_joined',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
