from django import forms


class UserLoginForm(forms.Form):
    email = forms.EmailField(required=True, label='E-mail')
    password = forms.CharField(required=True, label='Password', widget=forms.PasswordInput)
