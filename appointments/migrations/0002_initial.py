# Generated by Django 4.0.3 on 2022-03-29 13:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
        ('appointments', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointmentsmodel',
            name='patient',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='appointment', to='user.patient'),
        ),
        migrations.AddField(
            model_name='appointmentsmodel',
            name='professional',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='appointments', to='user.professional'),
        ),
    ]
