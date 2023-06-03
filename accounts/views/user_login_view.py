from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.views import View

from accounts.forms import UserLoginForm


class LoginView(View):
    form_class = UserLoginForm
    template_name = 'account/login.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('tour_list')
        return render(request, self.template_name, {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')
