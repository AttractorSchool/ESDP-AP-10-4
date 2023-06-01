import datetime

from choices import StatusChoice
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


def date_validation(value):
    if value < datetime.date.today():
        raise ValidationError('Нельзя выбрать дату из прошлого!')


class Tour(models.Model):
    author = models.ForeignKey(
        null=False,
        to=get_user_model(),
        related_name='tour',
        blank=False,
        verbose_name='Автор',
        on_delete=models.CASCADE,
    )
    title = models.CharField(
        max_length=300,
        null=False,
        blank=False,
        verbose_name='Название',
    )
    description = models.TextField(
        max_length=3000,
        null=False,
        blank=False,
        verbose_name='Описание',
    )
    start_date = models.DateField(
        auto_now_add=False,
        auto_now=False,
        verbose_name='Дата старта',
        validators=[date_validation],
    )
    end_date = models.DateField(
        auto_now_add=False,
        auto_now=False,
        verbose_name='Дата завершения',
        validators=[date_validation],
    )
    language = models.CharField(
        max_length=300,
        null=False,
        blank=False,
        verbose_name='Язык проведения',
    )
    price = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(1000000)],
        verbose_name='Стоимость',
    )
    max_number_of_tourists = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(250)],
        verbose_name='Максимальное количество туристов',
    )
    min_number_of_tourists = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(250)],
        verbose_name='Минимальное количество туристов',
    )
    moderation_status = models.CharField(
        max_length=256,
        null=False,
        choices=StatusChoice.choices,
        default=StatusChoice.NOT_VERIFIED,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата и время создания',
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата и время обновления',
    )
    tourists = models.ManyToManyField(
        to=get_user_model(),
        through='booking.Booking',
        related_name='booked_tour',
        through_fields=('tour', 'user'),
    )

    class Meta:
        verbose_name = 'Тур'
        verbose_name_plural = 'Туры'

    def get_deposit(self):
        return self.price / self.max_number_of_tourists

    def get_grand_total(self):
        tourists_count = self.tourists.count() + 1
        if tourists_count == 0:
            return self.price

        return round(self.price / tourists_count, 2)

    def get_grand_total_for_booking(self):
        tourists_count = self.tourists.count()
        grand_total = (self.price / tourists_count) - self.get_deposit()
        return round(grand_total, 2)

    def __str__(self):
        return f'Tour {self.title} by {self.author}'
