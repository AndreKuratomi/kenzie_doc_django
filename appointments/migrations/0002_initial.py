# Generated by Django 4.0.3 on 2022-03-27 15:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('appointments', '0001_initial'),
        ('user', '0001_initial'),
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
