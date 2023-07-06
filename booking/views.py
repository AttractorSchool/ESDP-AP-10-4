from booking.forms.passengers import PassengerForm
from booking.models import Booking
from choices.status_choices import StatusChoice, BookingChoice
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import ValidationError
from django.forms import formset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView
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

        passengers_count = 1
        if request.POST.get('passengers'):
            passengers_count = int(request.POST.get('passengers'))

        if passengers_count > tour.get_free_place():
            raise ValidationError('Вы превысили допустимое кол-во пассажиров!')

        # booking = Booking.objects.create(
        #     user=request.user,
        #     tour=tour,
        #     booking_status=BookingChoice.CREATED,
        # )

        # passenger = Passenger.objects.create(
        #     first_name=request.user.first_name,
        #     last_name=request.user.last_name,
        #     birthdate=request.user.birthdate,
        #     booking=Booking.objects.get(user=request.user, tour=tour),
        # )

        return redirect('add_passengers', pk=pk, passengers_count=passengers_count)

    def get(self):
        return redirect('tour_list')

    def test_func(self):
        if not self.request.user.is_guide and self.request.user.is_authenticated:
            if self.get_object().moderation_status in ALLOW_TO_BOOK_OR_CANCEL:
                return True
        else:
            return False


class AddPassengersView(View):
    def post(self, request, pk, passengers_count):
        # booking = get_object_or_404(Booking, pk=pk)
        tour = get_object_or_404(Tour, pk=pk)
        PassengerFormSet = formset_factory(PassengerForm, extra=passengers_count)
        formset = PassengerFormSet(request.POST)

        if formset.is_valid():
            booking = Booking.objects.create(
                user=request.user,
                tour=tour,
                booking_status=BookingChoice.CREATED,
            )

            for form in formset:
                passengers = form.save(commit=False)

                # if passengers.first_name and passengers.last_name and passengers.birthdate:
                passengers.booking = booking
                passengers.save()

            return HttpResponseRedirect(reverse('recarring') + f'?tour_id={tour.pk}')

        return render(request, 'passengers_form/passenger_form.html', {'formset': formset})

    def get(self, request, pk, passengers_count):
        PassengerFormSet = formset_factory(PassengerForm, extra=passengers_count-1)
        formset = PassengerFormSet(
            initial=[
                {
                    'first_name': request.user.first_name,
                    'last_name': request.user.last_name,
                    'birthdate': request.user.birthdate,
                },
            ],
        )

        return render(request, 'passengers_form/passenger_form.html', {'formset': formset})


class RecarringView(TemplateView):
    template_name = 'tour/booking/recarring.html'
