from django.db import models


class TourImage(models.Model):
    tour = models.ForeignKey(
        to='tours.Tour',
        related_name='images',
        on_delete=models.CASCADE,
        verbose_name='Тур',
    )

    image = models.ImageField(
        null=True,
        blank=True,
        upload_to='images',
    )

    def __str__(self):
        return f'Тур: {self.tour.title} | Картинка: {self.image.url}'
