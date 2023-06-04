from django.contrib.auth import get_user_model

from accounts.forms.user_update_form import UserUpdateForm
from choices import StatusChoice
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from accounts.forms import GuideProfileUpdateForm

ALLOWED_TO_EDIT = [
    StatusChoice.NOT_VERIFIED,
    StatusChoice.SENT_TO_REWORK,
]


class UpdateGuide(UserPassesTestMixin, UpdateView):
    model = get_user_model()
    form_class = UserUpdateForm
    template_name = 'account/update_guide.html'
    context_object_name = 'user_obj'
    success_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        if 'profile_form' not in kwargs:
            kwargs['profile_form'] = self.get_profile_form()
        return super().get_context_data(**kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.guide_profile.verification_status = StatusChoice.SENT_TO_VERIFICATION
        form = self.get_form()
        profile_form = self.get_profile_form()
        if form.is_valid() and profile_form.is_valid():
            return self.form_valid(form, profile_form)
        else:
            return self.form_invalid(form, profile_form)

    def form_valid(self, form, profile_form):
        response = super().form_valid(form)
        profile_form.save()
        return response

    def form_invalid(self, form, profile_form):
        context = self.get_context_data(form=form, profile_form=profile_form)
        return self.render_to_response(context)

    def get_profile_form(self):
        form_kwargs = {'instance': self.object.guide_profile}
        if self.request.method == 'POST':
            form_kwargs['data'] = self.request.POST
            form_kwargs['files'] = self.request.FILES
        return GuideProfileUpdateForm(**form_kwargs)

    def test_func(self):
        if self.request.user == self.get_object():
            if self.get_object().guide_profile.verification_status in ALLOWED_TO_EDIT:
                return True

        return False
