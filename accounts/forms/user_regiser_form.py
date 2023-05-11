from django import forms
from django.core.exceptions import ValidationError

from accounts.models import CustomUser


class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(required=True, widget=forms.PasswordInput)
    password_confirm = forms.CharField(required=True, widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'password', 'password_confirm')

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        if password_confirm and password and password != password_confirm:
            raise ValidationError('Пароли не совпадают')

    def save(self, commit=True):
        user = super().save(commit=True)
        user.set_password(self.cleaned_data.get('password'))
        return user
