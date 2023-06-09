from choices import BookingChoice
from django.contrib.auth import get_user_model
from django.db import models


# Create your models here.
class Booking(models.Model):
    user = models.ForeignKey(
        to=get_user_model(),
        related_name='tours',
        on_delete=models.CASCADE,
        verbose_name='Турист',
    )

    tour = models.ForeignKey(
        to='tours.Tour',
        related_name='users',
        on_delete=models.CASCADE,
        verbose_name='Тур',
    )
    booking_status = models.CharField(
        max_length=256,
        null=False,
        choices=BookingChoice.choices,
        default=BookingChoice.SENT_TO_VERIFICATION,
    )

    def hold_sum(self):
        return self.passengers.count() * self.tour.max_seat_hold_price()

    def __str__(self):
        return f'{self.user} | {self.tour}'


class Passenger(models.Model):
    first_name = models.CharField(
        max_length=256,
        blank=True,
        null=True,
        verbose_name='Имя пассажира',
    )

    last_name = models.CharField(
        max_length=256,
        blank=True,
        null=True,
        verbose_name='Фамилия пассажира',
    )

    birthdate = models.DateField(null=True, blank=True)

    booking = models.ForeignKey(
        to='booking.Booking',
        related_name='passengers',
        on_delete=models.CASCADE,
        null=True,
        verbose_name='Бронирование',
    )

    def __str__(self):
        return f'{self.booking} {self.first_name} {self.last_name} {self.birthdate}'
