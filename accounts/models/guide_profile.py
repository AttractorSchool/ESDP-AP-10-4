from choices import ProfileStatusChoice
from django.contrib.auth import get_user_model
from django.db import models


class GuideProfile(models.Model):
    user = models.OneToOneField(
        to=get_user_model(),
        related_name='guide_profile',
        on_delete=models.CASCADE,
        verbose_name='Пользователь')

    verification_status = models.CharField(
        max_length=256,
        null=False,
        choices=ProfileStatusChoice.choices,
        default=ProfileStatusChoice.NOT_VERIFIED)

    current_location = models.CharField(
        null=False,
        blank=False,
        max_length=512)

    languages = models.CharField(
        null=False,
        blank=False,
        max_length=512,
        verbose_name='Языки')

    about = models.TextField(
        null=False,
        blank=False,
        max_length=2048,
        verbose_name='О себе')

    experience_resume = models.FileField(
        null=False,
        blank=False,
        upload_to='experience_resumes',
        verbose_name='Резюме с опытом')

    certificates = models.FileField(
        null=False,
        blank=False,
        upload_to='certificates',
        verbose_name='Сертификаты')

    bank_details = models.CharField(
        null=False,
        blank=False,
        max_length=512)

    def __str__(self):
        return f'Гид: {self.user} | Status: {self.verification_status}'
