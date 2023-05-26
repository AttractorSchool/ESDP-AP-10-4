from django.shortcuts import get_object_or_404

from choices import StatusChoice
from django.views.generic import DetailView

from accounts.models import Profile


class GuideProfileView(DetailView):
    model = Profile
    template_name = 'guide_profile.html'
    context_object_name = 'user_obj'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(verification_status=StatusChoice.CONFIRMED)
        return queryset
