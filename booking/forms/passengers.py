from django import forms
from booking.models import Passenger


class PassengerForm(forms.ModelForm):

    class Meta:
        model = Passenger
        fields = ('first_name', 'last_name', 'birthdate')
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'birthdate': 'Дата рождения',
        }
        widgets = {
            'birthdate': forms.DateInput(
                format=('%Y-%m-%d'),
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Выберите дату',
                    'type': 'date',
                },
            ),
        }
