from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
# from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import RegisterUserForm, LoginUserForm


class Register(CreateView):
    template_name = 'registration.html'
    form_class = RegisterUserForm
    success_url = '/login/'


class Login(LoginView):
    template_name = 'login.html'
    form_class = LoginUserForm


    # def get_success_url(self):
    #     return reverse_lazy('/')


def logout_user(request):
    logout(request)
    return redirect('/')