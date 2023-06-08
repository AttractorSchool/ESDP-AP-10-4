from django.urls import path

from .views import LoginView, logout_view
from .views import RegisterView
from .views.guide_profile_index import GuideProfileView
from .views.tourist_profile_view import TouristDetailView
from .views.update_guide import UpdateGuide


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('guide-profile/<int:pk>', GuideProfileView.as_view(), name='guide_profile'),
    path('tourist-profile/<int:pk>', TouristDetailView.as_view(), name='tourist-profile'),
    path('update/<int:pk>', UpdateGuide.as_view(), name='update_guide'),
]
