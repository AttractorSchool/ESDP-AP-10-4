from booking.forms.passengers import PassengerForm
from booking.models import Booking
from booking.models import Passenger
from choices.status_choices import StatusChoice, BookingChoice
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import CreateView
from django.views.generic.detail import SingleObjectMixin
from tours.models import Tour

ALLOW_TO_BOOK_OR_CANCEL = [
    StatusChoice.CONFIRMED,
]


class BookToursView(UserPassesTestMixin, SingleObjectMixin, View):
    model = Tour

    def post(self, request, pk):
        tour = get_object_or_404(self.model, pk=pk)

        if request.user in tour.tourists.all():
            Booking.objects.filter(user=request.user, tour=tour).delete()
            return redirect('tour_detail', pk=pk)

        booking = Booking.objects.create(
            user=request.user,
            tour=tour,
            booking_status=BookingChoice.RESERVED,
        )

        return redirect('add_passengers', pk=booking.pk)

    def get(self):
        return redirect('tour_list')

    def test_func(self):
        if not self.request.user.is_guide and self.request.user.is_authenticated:
            if self.get_object().moderation_status in ALLOW_TO_BOOK_OR_CANCEL:
                return True
        else:
            return False


class AddPassengersView(CreateView):
    template_name = 'passengers_form/passenger_form.html'
    model = Passenger
    form_class = PassengerForm

    def form_valid(self, form):
        booking = get_object_or_404(Booking, pk=self.kwargs.get('pk'))
        passengers = form.save(commit=False)
        passengers.booking = booking
        passengers.save()
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse('tourist_profile', kwargs={'pk': self.request.user.pk})
