from django import forms
from django.core.exceptions import ValidationError

from django.contrib.auth import get_user_model


class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(required=True, widget=forms.PasswordInput)
    password_confirm = forms.CharField(required=True, widget=forms.PasswordInput)
    is_guide = forms.BooleanField(required=False)

    class Meta:
        model = get_user_model()
        fields = ('email', 'first_name', 'last_name', 'password', 'password_confirm', 'is_guide')

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        if password_confirm and password and password != password_confirm:
            raise ValidationError('Пароли не совпадают')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get('password'))

        if not user.is_guide:
            user.is_tourist = True

        if commit:
            user.save()
        return user
