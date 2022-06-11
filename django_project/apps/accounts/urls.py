from django.urls import path
from .views import Register, Login, logout_user


urlpatterns = [
    path('login/', Login.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('registration/', Register.as_view(), name='registration'),
]