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

    def __str__(self):
        return f'{self.user} | {self.tour}'
