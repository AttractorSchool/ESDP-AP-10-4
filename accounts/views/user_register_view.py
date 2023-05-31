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
        form = self.form_class(request.POST)
        if form.is_valid():
            user = create_profile(form)
            login(request, user)
            return redirect('/admin')
        self.context['form'] = form
        return self.render_to_response(self.context)
