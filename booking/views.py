from django.views import View
from django.views.generic import TemplateView

from booking.models import Booking
from choices import StatusChoice
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
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

        Booking.objects.create(
            user=request.user,
            tour=tour,
        )

        return redirect('tour_detail', pk=pk)

    def get(self, request, *args, **kwargs):
        return redirect('tour_list')

    def test_func(self):
        if not self.request.user.is_guide and self.request.user.is_authenticated:
            if self.get_object().moderation_status in ALLOW_TO_BOOK_OR_CANCEL:
                return True
        else:
            return False


class RecarringView(TemplateView):
    template_name = "tour/booking/recarring.html"

    # get_cont
    #
    # # def get(self, request, *args, **kwargs):
    #

