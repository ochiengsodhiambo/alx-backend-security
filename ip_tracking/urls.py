from django.urls import path
from .views import login_authenticated, login_anonymous

urlpatterns = [
    path('login-auth/', login_authenticated),
    path('login-public/', login_anonymous),
]