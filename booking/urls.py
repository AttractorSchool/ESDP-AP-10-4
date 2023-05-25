from booking.views import book_tours
from django.urls import path

urlpatterns = [
    path('<int:pk>', book_tours, name='book_tours'),
]
