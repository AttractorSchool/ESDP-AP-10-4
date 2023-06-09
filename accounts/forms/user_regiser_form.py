from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError


class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput,
        label='Create password',
    )

    password_confirm = forms.CharField(
        required=True,
        widget=forms.PasswordInput,
        label='Password confirm',
    )

    is_guide = forms.BooleanField(required=False)

    class Meta:
        model = get_user_model()
        fields = ('email', 'first_name', 'last_name', 'password', 'password_confirm', 'is_guide')

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        if password_confirm and password and password != password_confirm:
            raise ValidationError('')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get('password'))

        if not user.is_guide:
            user.is_tourist = True

        if commit:
            user.save()
        return user
