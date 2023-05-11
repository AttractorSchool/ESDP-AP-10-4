from django.contrib.auth import login
from django.shortcuts import redirect
from django.views.generic import CreateView

from accounts.forms import UserRegisterForm


class RegisterView(CreateView):
    template_name = 'register.html'
    form_class = UserRegisterForm
    success_url = '/admin'

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            user.profile.is_guide = form.cleaned_data.get('is_guide')
            user.profile.save()
            login(request, user)
            return redirect('/admin')
        context = dict()
        context['form'] = form
        return self.render_to_response(context)
