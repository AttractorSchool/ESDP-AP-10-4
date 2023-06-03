from booking.models import Booking
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from tours.models import Tour
from django.contrib.auth.mixins import UserPassesTestMixin


class BookToursView(UserPassesTestMixin, View):
    def post(self, request, pk):
        tour = get_object_or_404(Tour, pk=pk)

        if request.user in tour.tourists.all():
            Booking.objects.filter(user=request.user, tour=tour).delete()
            return redirect('tour_detail', pk=pk)

        Booking.objects.create(
            user=request.user,
            tour=tour,
        )

        return redirect('tour_detail', pk=pk)

    def get(self):
        return redirect('tour_list')

    def test_func(self):
        if not self.request.user.is_guide and self.request.user.is_authenticated:
            return True
        else:
            return False
