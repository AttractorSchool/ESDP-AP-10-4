from django import forms
from tours.models import TourImage


class TourImageForm(forms.ModelForm):
    class Meta:
        model = TourImage
        fields = ['image']
        widgets = {
            'image': forms.ClearableFileInput(attrs={
                'multiple': True,
            })
        }
