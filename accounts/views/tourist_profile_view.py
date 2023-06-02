from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import DetailView
from django.contrib.auth import get_user_model


class TouristDetailView(UserPassesTestMixin, DetailView):
    model = get_user_model()
    template_name = 'account/tourist_profile.html'
    context_object_name = 'user_obj'

    def test_func(self):
        return self.request.user.is_authenticated
