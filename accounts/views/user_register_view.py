from django.contrib.auth import login
from django.shortcuts import redirect
from django.views.generic import CreateView

from accounts.forms import UserRegisterForm
from accounts.utils import create_profile


class RegisterView(CreateView):
    template_name = 'account/register.html'
    form_class = UserRegisterForm
    success_url = '/admin'
    context = dict()

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            create_profile(user)
            login(request, user)
            return redirect('tour_list')
        self.context['form'] = form
        form.add_error('password', '')
        form.add_error('password_confirm', 'Пароли не совпадают')
        return self.render_to_response(self.context)
