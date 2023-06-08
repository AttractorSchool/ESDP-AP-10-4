from datetime import datetime, timedelta

from choices import StatusChoice
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView
from tours.forms.tour_create_form import TourCreateForm
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


class TourListView(ListView):
    model = Tour
    context_object_name = 'tours'
    template_name = 'tour/tour_list.html'

    def get(self, request, *args, **kwargs):
        tours = Tour.objects.all()
        today = (datetime.now() + timedelta(hours=6)).strftime('%Y-%m-%d %H:%M')
        for tour in tours:
            if today >= tour.end_date.strftime('%Y-%m-%d %H:%M'):
                tour.moderation_status = StatusChoice.FINISHED
            tour.save()
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super(TourListView, self).get_queryset()
        return queryset.filter(moderation_status='CONFIRMED')


class TourCreateView(CreateView):
    template_name = 'tour/tour_create.html'
    model = Tour
    form_class = TourCreateForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.moderation_status = StatusChoice.SENT_TO_VERIFICATION
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('tour_detail', kwargs={'pk': self.object.pk})

    def test_func(self):
        if self.request.user.is_authenticated:
            if self.request.user.is_guide \
                    and self.request.user.guide_profile.verification_status == StatusChoice.CONFIRMED:
                return True
        else:
            return False
        return False


class TourDetailView(UserPassesTestMixin, DetailView):
    template_name = 'tour/tour_detail.html'
    model = Tour
    context_object_name = 'tour'

    def get(self, request, pk, *args, **kwargs):
        tour = get_object_or_404(self.model, pk=pk)
        today = (datetime.now() + timedelta(hours=6)).strftime('%Y-%m-%d %H:%M')
        start_date = tour.start_date.strftime('%Y-%m-%d %H:%M')
        end_date = tour.end_date.strftime('%Y-%m-%d %H:%M')

        if today >= start_date:
            tour.moderation_status = StatusChoice.STARTED

        if today >= end_date:
            tour.moderation_status = StatusChoice.FINISHED

        tour.save()
        return super().get(request, *args, **kwargs)

    def test_func(self):
        if self.request.user == self.get_object().author:
            return True
        elif self.request.user != self.get_object().author \
                and self.get_object().moderation_status in ALLOWED_TO_VIEW:
            return True
        else:
            return False


class TourUpdateView(UserPassesTestMixin, UpdateView):
    template_name = 'tour/tour_update.html'
    model = Tour
    form_class = TourCreateForm

    def get_success_url(self):
        return reverse('tour_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        form.instance.moderation_status = StatusChoice.SENT_TO_VERIFICATION
        return super().form_valid(form)

    def test_func(self):
        if self.get_object().author == self.request.user:
            if self.get_object().moderation_status in ALLOWED_TO_EDIT:
                return True
        return False


class TourDeleteView(UserPassesTestMixin, DeleteView):
    model = Tour

    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'pk': self.object.author_id})

    def test_func(self):
        if self.get_object().author == self.request.user \
                and self.get_object().moderation_status == StatusChoice.CONFIRMED:
            return True
        return False
