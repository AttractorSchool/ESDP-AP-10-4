from booking.views import BookToursView, AddPassengersView
from django.urls import path

urlpatterns = [
    path('<int:pk>', BookToursView.as_view(), name='create_booking'),
    path('<int:pk>/add_passengers', AddPassengersView.as_view(), name='add_passengers'),
]
