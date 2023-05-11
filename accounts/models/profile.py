from django.contrib.auth import get_user_model
from django.db import models

from accounts.choices import GuideProfileStatus


class Profile(models.Model):
    user = models.OneToOneField(
        to=get_user_model(),
        related_name='profile',
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
    )

    is_guide = models.BooleanField(null=False, default=False)

    verification_status = models.CharField(
        max_length=256,
        null=False,
        choices=GuideProfileStatus.choices,
        default=GuideProfileStatus.NOT_VERIFIED,
    )

    current_location = models.CharField(
        null=True,
        blank=True,
        max_length=512,
    )

    birthdate = models.DateField(null=True, blank=False)

    languages = models.CharField(
        null=True,
        blank=True,
        max_length=512,
        verbose_name='Языки',
    )

    about = models.TextField(
        null=True,
        blank=True,
        max_length=2048,
        verbose_name='О себе',
    )

    experience_resume = models.FileField(
        null=True,
        blank=True,
        upload_to='experience_resumes',
        verbose_name='Резюме с опытом',
    )

    certificates = models.FileField(
        null=True,
        blank=True,
        upload_to='certificates',
        verbose_name='Сертификаты',
    )

    bank_details = models.CharField(max_length=512)

    def __str__(self):
        return f'User: {self.user} | Is Guide:{self.is_guide} | Status: {self.verification_status}'
