# Generated by Django 4.2.2 on 2023-06-15 17:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tours', '0006_alter_tourrating_text_review'),
        ('booking', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='tour',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='users', to='tours.tour', verbose_name='Тур'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='booking',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='tours', to=settings.AUTH_USER_MODEL, verbose_name='Турист'),
            preserve_default=False,
        ),
    ]
