from django import forms
from django.contrib.auth.forms import (AuthenticationForm, UserChangeForm,
                                       UserCreationForm)
from django.contrib.auth import get_user_model


class UserLoginForm(AuthenticationForm):
    class Meta:
        model = get_user_model
        fields = ('username', 'password')


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password1', 'password2')
