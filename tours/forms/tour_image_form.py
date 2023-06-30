from django import forms
from tours.models import TourImage


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class TourImageForm(forms.ModelForm):
    image = forms.ImageField(
        required=False,
        widget=MultipleFileInput(),
    )

    class Meta:
        model = TourImage
        fields = ['image']
