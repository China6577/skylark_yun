# Generated by Django 5.1.7 on 2025-03-20 10:12

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0002_usercourse'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
