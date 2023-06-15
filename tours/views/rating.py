from choices import StatusChoice
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect
from django.views import View
from django.views.generic.detail import SingleObjectMixin
from tours.forms.tour_rating_create_form import TourRatingCreateForm
from tours.models.tour import Tour


class TourRatingCreateView(UserPassesTestMixin, SingleObjectMixin, View):
    model = Tour

    def post(self, request, pk):
        form = TourRatingCreateForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.tour_id = pk
            form.tourist = request.user
            form.save()
        return redirect(request.META.get('HTTP_REFERER'))

    def test_func(self):
        tour_ratings = self.get_object().tour_rating.all()
        is_participated = self.request.user in self.get_object().tourists.all()
        tourist_reviewed = [rating.tourist for rating in tour_ratings]

        if self.get_object().moderation_status == StatusChoice.FINISHED:
            if is_participated and self.request.user not in tourist_reviewed:
                return True
            return False
