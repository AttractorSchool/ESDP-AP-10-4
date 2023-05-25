from booking.models import Booking
from django.shortcuts import get_object_or_404, redirect
from tours.models import Tour


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
