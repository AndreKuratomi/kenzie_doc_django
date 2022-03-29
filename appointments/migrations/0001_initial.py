# Generated by Django 4.0.3 on 2022-03-29 12:10

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AppointmentsModel',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('complaint', models.CharField(default='', max_length=255)),
                ('finished', models.BooleanField(default=False)),
            ],
        ),
    ]
