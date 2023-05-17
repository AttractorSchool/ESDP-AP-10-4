from django import forms
from tours.models.tour import Tour


class TourCreateForm(forms.ModelForm):
    class Meta:
        model = Tour
        fields = (
            'title',
            'description',
            'start_date',
            'end_date',
            'language',
            'price',
            'max_number_of_tourists',
            'min_number_of_tourists'
        )
        labels = {
            'title': 'Название тура',
            'description': 'Описание тура',
            'start_date': 'Дата и время старта тура',
            'end_date': 'Дата и время окончания тура',
            'language': 'Язык проведения тура',
            'price': 'Цена тура',
            'max_number_of_tourists': 'Максимальное количество туристов',
            'min_number_of_tourists': 'Минимальное количество туристов'
        }
        widgets = {
            'start_date': forms.DateInput(
                format=('%Y-%m-%d'),
                attrs={'class': 'form-control',
                       'placeholder': 'Select a date',
                       'type': 'date'
                       }),
            'end_date': forms.DateInput(
                format=('%Y-%m-%d'),
                attrs={'class': 'form-control',
                       'placeholder': 'Select a date',
                       'type': 'date'
                       }),
        }
