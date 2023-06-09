# Generated by Django 4.2.2 on 2023-06-09 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='guideprofile',
            name='verification_status',
            field=models.CharField(choices=[('NOT VERIFIED', 'Непроверен'), ('SENT TO VERIFICATION', 'Отправлен на проверку'), ('SENT TO REWORK', 'Отправлен на доработку'), ('CONFIRMED', 'Подтвержден'), ('REFUSED', 'Отказ'), ('FINISHED', 'Завершён'), ('STARTED', 'Начался')], default='NOT VERIFIED', max_length=256),
        ),
    ]
