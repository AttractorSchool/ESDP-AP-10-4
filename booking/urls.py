from booking.views import BookToursView, AddPassengersView
from django.urls import path

urlpatterns = [
    path('<int:pk>/', BookToursView.as_view(), name='create_booking'),
    path('<int:pk>/add_passengers/<int:passengers_count>', AddPassengersView.as_view(), name='add_passengers'),
]
