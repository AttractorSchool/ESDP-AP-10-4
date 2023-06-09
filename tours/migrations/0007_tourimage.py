# Generated by Django 4.2.2 on 2023-06-28 16:48

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tours', '0006_alter_tourrating_text_review'),
    ]

    operations = [
        migrations.CreateModel(
            name='TourImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='images', validators=[django.core.validators.FileExtensionValidator(['png', 'jpeg'])])),
                ('tour', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='tours.tour', verbose_name='Тур')),
            ],
        ),
    ]
