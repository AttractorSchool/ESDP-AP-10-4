from booking.views import BookToursView
from django.urls import path

urlpatterns = [
    path('<int:pk>', BookToursView.as_view(), name='book_tours'),
]
