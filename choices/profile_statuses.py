from django.db import models


class ProfileStatusChoice(models.TextChoices):
    """
    Непроверен
    Отправлен на проверку
    Отправлен на доработку
    Отказ
    Подтвержден

    """

    NOT_VERIFIED = 'NOT VERIFIED', 'Непроверен'
    SENT_TO_VERIFICATION = 'SENT TO VERIFICATION', 'Отправлен на проверку'
    SENT_TO_REWORK = 'SENT TO REWORK', 'Отправлен на доработку'
    CONFIRMED = 'CONFIRMED', 'Подтвержден'
    REFUSED = 'REFUSED', 'Отказ'
