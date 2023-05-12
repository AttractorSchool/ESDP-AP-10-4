from django import forms
from django.core.exceptions import ValidationError

from accounts.models import CustomUser
from accounts.models.profile import Profile


class UserLoginForm(forms.Form):
    email = forms.EmailField(required=True, label='E-mail')
    password = forms.CharField(required=True, label='Password', widget=forms.PasswordInput)


class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(required=True, widget=forms.PasswordInput)
    password_confirm = forms.CharField(required=True, widget=forms.PasswordInput)
    is_guide = forms.BooleanField(required=False)

    class Meta:
        model = CustomUser
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
        if commit:
            user.save()
            Profile.objects.create(user=user)
        return user
