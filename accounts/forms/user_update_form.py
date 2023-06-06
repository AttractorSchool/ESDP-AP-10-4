from django import forms
from django.contrib.auth import get_user_model


class DateInput(forms.DateInput):
    input_type = 'date'


class UserUpdateForm(forms.ModelForm):
    birthdate = forms.DateField(widget=DateInput)

    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'birthdate']
