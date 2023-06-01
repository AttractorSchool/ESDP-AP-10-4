from django.urls import path
from .views import RegisterView
from .views import LoginView, logout_view
from .views.guide_profile_index import GuideProfileView
from .views.tourist_profile_view import TouristDetailView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    # path('update-profile/<int:pk>', UpdateGuideProfile.as_view(), name='update_guide_profile'),
    path('guide-profile/<int:pk>', GuideProfileView.as_view(), name='guide-profile'),
    # path('tourist-profile/<int:pk>', TouristDetailView.as_view(), name='tourist-profile'),
]
