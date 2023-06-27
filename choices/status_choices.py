from django.db import models


class StatusChoice(models.TextChoices):
    """
    Непроверен
    Отправлен на проверку
    Отправлен на доработку
    Отказ
    Подтвержден
    Завершён
    Начался
    """

    NOT_VERIFIED = 'NOT VERIFIED', 'Непроверен'
    SENT_TO_VERIFICATION = 'SENT TO VERIFICATION', 'Отправлен на проверку'
    SENT_TO_REWORK = 'SENT TO REWORK', 'Отправлен на доработку'
    CONFIRMED = 'CONFIRMED', 'Подтвержден'
    REFUSED = 'REFUSED', 'Отказ'
    FINISHED = 'FINISHED', 'Завершён'
    STARTED = 'STARTED', 'Начался'


class BookingChoice(models.TextChoices):
    CREATED = 'CREATED', 'Создан'
    RESERVED = 'RESERVED', 'Зарезервирован'
    HOLD = 'HOLD', 'Удержано'
    CANCELED = 'CANCELED', 'Отменено'
    SENT_TO_VERIFICATION = 'SENT TO VERIFICATION', 'Отправлен на проверку'
