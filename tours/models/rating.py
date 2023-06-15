from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class TourRating(models.Model):
    tourist = models.ForeignKey(
        to=get_user_model(),
        related_name='rating_by_tourist',
        on_delete=models.CASCADE,
    )
    tour = models.ForeignKey(
        to='tours.Tour',
        related_name='tour_rating',
        on_delete=models.CASCADE,
    )
    correspondence = models.SmallIntegerField(
        blank=False,
        null=False,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name='Соответствие тура описанию',
    )
    professionalism = models.SmallIntegerField(
        blank=False,
        null=False,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name='Профессионализм гида',
    )
    text_review = models.TextField(
        max_length=3000,
        null=True,
        blank=True,
        verbose_name='Текстовый отзыв',
    )

    class Meta:
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинги'

    def __str__(self):
        return f'{self.tour}: {self.professionalism}, {self.correspondence}'
