from django.contrib import auth
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView
from django.contrib.auth.models import User


# Create your views here.

class UserLoginView(LoginView):
    template_name = 'users/login.html'


class UserRegistrationView(CreateView):
    model = get_user_model()
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')
    fields = ['username', 'email', 'password']