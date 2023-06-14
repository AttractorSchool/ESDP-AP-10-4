from django import forms
from tours.models.rating import TourRating


class TourRatingCreateForm(forms.ModelForm):

    class Meta:
        model = TourRating
        fields = (
            'correspondence',
            'professionalism',
            'text_review',
        )
        labels = {
            'correspondence': 'Соответстсвие тура описанию*',
            'professionalism': 'Профессионализм гида*',
            'text_review': 'Ваш комментарий',
        }
