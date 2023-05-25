from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.views.generic import DetailView

from choices import StatusChoice


class GuideProfileView(DetailView):
    model = get_user_model()
    template_name = 'guide_profile.html'
    context_object_name = 'user_obj'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(profile__verification_status=StatusChoice.CONFIRMED)
        return queryset




