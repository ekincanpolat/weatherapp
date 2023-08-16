from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import RegisterView, LoginView, LogoutView, UserProfileViewSet
from .base_view import create_view_paths

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    *create_view_paths('profile', UserProfileViewSet),
]