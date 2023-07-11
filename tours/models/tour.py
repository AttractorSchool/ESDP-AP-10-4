from datetime import datetime, timedelta

from choices import StatusChoice, BookingChoice
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


def date_validation(value):
    value_str = value.strftime('%Y-%m-%d %H:%M')
    datetime_now_str = datetime.now().strftime('%Y-%m-%d %H:%M')
    if value_str < datetime_now_str:
        raise ValidationError('Нельзя выбрать дату из прошлого!')


def validator_date(start_date, end_date):
    if start_date > end_date:
        raise ValidationError('Дата начала тура должна быть раньше даты завершения.')


def possibility_of_creating_a_tour(start_date):
    interval = start_date - datetime.now()
    three_days = timedelta(days=3)
    if interval < three_days:
        raise ValidationError('Нельзя создавать тур менее чем за 3 дня')


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
    start_date = models.DateTimeField(
        auto_now_add=False,
        auto_now=False,
        verbose_name='Дата старта',
        validators=[date_validation],
    )
    end_date = models.DateTimeField(
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

    def clean(self):
        validator_date(self.start_date, self.end_date)
        possibility_of_creating_a_tour(self.start_date)

    # def get_deposit(self):
    #     return round(self.price / self.max_number_of_tourists)
    #
    # def get_grand_total(self):
    #     tourists_count = self.tourists.count() + 1
    #     if tourists_count == 0:
    #         return self.price
    #
    #     return round(self.price / tourists_count)
    #
    # def get_grand_total_for_booking(self):
    #     tourists_count = self.tourists.count()
    #     grand_total = (self.price / tourists_count) - self.get_deposit()
    #     return round(grand_total)

    @property
    def average_rating(self):
        lst = []
        for rating in self.tour_rating.all():
            lst.append(rating.professionalism)
            lst.append(rating.correspondence)
        try:
            avg = sum(lst) / len(lst)
        except ZeroDivisionError:
            return 0
        return round(avg, 1)

    def get_free_place(self):
        active_passengers_count = self.max_number_of_tourists
        for passenger in self.users.filter(booking_status__in=[BookingChoice.RESERVED, BookingChoice.HOLD, BookingChoice.PAYED]):
            if passenger.passengers:
                active_passengers_count = active_passengers_count - passenger.passengers.count()
        return active_passengers_count

    def max_seat_hold_price(self):
        return self.price / self.min_number_of_tourists

    def seat_charge_price(self):
        return self.price / self.booking_tourist_count()

    def booking_tourist_count(self):
        for passenger in self.users.filter(booking_status__in=[BookingChoice.HOLD, BookingChoice.PAYED]):
            if passenger.passengers:
                return passenger.passengers.count()
        return 0

    def __str__(self):
        return f'Tour {self.title} by {self.author}'
