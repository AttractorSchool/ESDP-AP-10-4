from django.urls import path
from .views import RegisterView
from .views import LoginView, logout_view
from .views.update_guide import UpdateGuide

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('update/<int:pk>', UpdateGuide.as_view(), name='update_guide'),
]
