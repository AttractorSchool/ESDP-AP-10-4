from django import forms
from django.core.validators import FileExtensionValidator

from accounts.models import GuideProfile


class GuideProfileUpdateForm(forms.ModelForm):
    experience_resume = forms.FileField(
        validators=[FileExtensionValidator(['pdf'])],
        help_text='загрузите свое резюме 1 файлом в формате PDF',
    )
    certificates = forms.FileField(help_text='загрузите все свои сертификаты 1 фалом в формате PDF')

    class Meta:
        model = GuideProfile
        fields = (
            'current_location',
            'languages',
            'about',
            'experience_resume',
            'certificates',
            'bank_details',
        )
        required = (
            'current_location',
            'languages',
            'about',
            'experience_resume',
            'certificates',
            'bank_details',
        )
