from choices import StatusChoice
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView
from django.views.generic.detail import SingleObjectMixin
from tours.forms.tour_rating_create_form import TourRatingCreateForm
from tours.models.tour import Tour

ALLOWED_TO_VIEW = [
    StatusChoice.CONFIRMED,
    StatusChoice.FINISHED,
    StatusChoice.STARTED,
]

ALLOWED_TO_EDIT = [
    StatusChoice.NOT_VERIFIED,
    StatusChoice.SENT_TO_REWORK,
]


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
        if self.request.user.is_authenticated and self.get_object().moderation_status == StatusChoice.FINISHED:
            if self.request.user in self.get_object().tourists.all():
                return True
        return False
