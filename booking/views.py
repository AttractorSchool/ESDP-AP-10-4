from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView

from tours.models import Tour
from booking.models import Booking


# Create your views here.
def book_tours(request, pk):
    if request.method == 'POST':
        tour = get_object_or_404(Tour, pk=pk)

        if request.user in tour.tourists.all():
            return redirect('tour_detail', pk=pk)

        Booking.objects.create(
            user=request.user,
            tour=tour,
        )

        return redirect('tour_detail', pk=pk)

    return redirect('tour_list')
