from booking.views import BookToursView, RecarringView
from django.urls import path

urlpatterns = [
    path('<int:pk>', BookToursView.as_view(), name='book_tours'),
    path('<int:pk>/recarring', RecarringView.as_view(), name='recarring'),
]
