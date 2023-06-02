from choices import StatusChoice
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import Http404
from django.views.generic import DetailView

from accounts.models import GuideProfile


class GuideProfileView(UserPassesTestMixin, DetailView):
    model = GuideProfile
    template_name = 'account/guide_profile.html'
    context_object_name = 'user_obj'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        verification_status = self.object.verification_status
        context['is_verified'] = verification_status == StatusChoice.CONFIRMED
        return context

    def test_func(self):
        if self.request.user.is_authenticated:
            obj = self.get_object()
            if self.request.user == obj.user or self.request.user.is_superuser:
                return True
            elif obj.verification_status == StatusChoice.CONFIRMED:
                return True
        raise Http404('Пользователь не найден')
