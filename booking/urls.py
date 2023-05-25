from django.urls import path

from booking.views import book_tours

urlpatterns = [
    path('<int:pk>', book_tours, name='book_tours'),
]
