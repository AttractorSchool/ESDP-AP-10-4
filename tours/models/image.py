from django.db import models


class TourImage(models.Model):
    tour = models.ForeignKey(
        to='tours.Tour',
        related_name='images',
        on_delete=models.CASCADE,
        verbose_name='Тур',
    )

    image = models.ImageField(
        upload_to='images/{tour_title}'.format(tour_title=tour.title),
    )

    def __str__(self):
        return f'{self.tour.title} {self.image.url}'
