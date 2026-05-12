from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView
from . import forms
from django.contrib.auth import login
from django.contrib.auth.views import LoginView,LogoutView

# Create your views here.

class UserRegistrationView(FormView):
    template_name='user_registration.html'
    form_class=forms.UserRegistrationForm
    success_url=reverse_lazy('home')

    def form_valid(self,form):
        user=form.save()
        login(self.request,user)
        return super().form_valid(form)

class UserLoginView(LoginView):
    template_name='user_login.html'
    success_url=reverse_lazy('home')     


class UserLogoutView(LogoutView):
    next_page=reverse_lazy('home')    



