from django.urls import path
# from accounts.views import LoginView, logout_view, RegisterView, UpdateGuideProfile
from .views import LoginView, logout_view

urlpatterns = [
    # path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    # path('update-profile/<int:pk>', UpdateGuideProfile.as_view(), name='update_guide_profile'),
]
