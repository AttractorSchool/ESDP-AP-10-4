# Generated by Django 4.2.1 on 2023-05-31 15:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='guideprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='guide_profile', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
    ]
