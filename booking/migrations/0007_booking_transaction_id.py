# Generated by Django 4.2.3 on 2023-07-06 00:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0006_alter_passenger_birthdate_alter_passenger_first_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='transaction_id',
            field=models.SmallIntegerField(blank=True, null=True, verbose_name='ID транзакции CP'),
        ),
    ]
