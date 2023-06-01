from django.urls import path
from .views import RegisterView
from .views import LoginView, logout_view
from .views.guide_profile_index import GuideProfileView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    # path('update-profile/<int:pk>', UpdateGuideProfile.as_view(), name='update_guide_profile'),
    path('profile/<int:pk>', GuideProfileView.as_view(), name='profile'),
]
