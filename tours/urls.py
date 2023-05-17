from django.urls import path
from tours.views.crud_tours import (
    TourCreateView,
    TourDeleteView,
    TourDetailView,
    TourUpdateView,
)

urlpatterns = [
    path('create/', TourCreateView.as_view(), name='tour_create'),
    path('<int:pk>/', TourDetailView.as_view(), name='tour_detail'),
    path('<int:pk>/update/', TourUpdateView.as_view(), name='tour_update'),
    path('<int:pk>/delete/', TourDeleteView.as_view(), name='tour_delete'),
]
