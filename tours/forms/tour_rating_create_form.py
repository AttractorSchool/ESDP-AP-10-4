from django import forms
from tours.models.rating import TourRating


class TourRatingCreateForm(forms.ModelForm):
    correspondence = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'type': 'number',
                'min': 0,
                'max': 5,
            }
        ),
        label='Соответстсвие тура описанию*',
    )

    professionalism = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'type': 'number',
                'min': 0,
                'max': 5,
            }
        ),
        label='Профессионализм гида*',
    )

    class Meta:
        model = TourRating
        fields = (
            'correspondence',
            'professionalism',
            'text_review',
        )
        labels = {
            'text_review': 'Ваш комментарий',
        }
