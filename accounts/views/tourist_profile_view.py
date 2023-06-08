from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import DetailView

from tours.models import Tour


class TouristDetailView(UserPassesTestMixin, DetailView):
    model = get_user_model()
    template_name = 'account/tourist_profile.html'
    context_object_name = 'user_obj'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tourist_tour_ids = self.object.tours.values_list('tour_id', flat=True)
        tourist_tours = Tour.objects.filter(id__in=tourist_tour_ids)
        context['tourist_tours'] = tourist_tours
        return context

    def test_func(self):
        return True

