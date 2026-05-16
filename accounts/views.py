from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView
from . import forms
from django.contrib.auth import login
from django.contrib.auth.views import LoginView,LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate
from django.contrib import messages
from django.shortcuts import redirect
from .models import EmailOTP
from .utils import send_otp_email
from django.contrib.auth.models import User
from .forms import OTPForm
from .models import EmailOTP



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

    template_name = 'user_login.html'

    def form_valid(self, form):

        username = form.cleaned_data['username']
        password = form.cleaned_data['password']

        user = authenticate(
            username=username,
            password=password
        )

        if user is not None:

            # Save user id in session
            self.request.session['user_id'] = user.id

            # Send OTP email
            send_otp_email(user)

            messages.success(
                self.request,
                'Verification code sent to your email.'
            )

            return redirect('verify_otp')

        return super().form_invalid(form)
    


class UserLogoutView(LogoutView):
    next_page=reverse_lazy('home')    



class ProfileView(LoginRequiredMixin, TemplateView):
    template_name='profile.html'





class VerifyOTPView(FormView):

    template_name = 'verify_otp.html'

    form_class = OTPForm

    success_url = reverse_lazy('home')

    def form_valid(self, form):

        entered_otp = form.cleaned_data['otp']

        user_id = self.request.session.get('user_id')

        user = User.objects.get(id=user_id)

        otp_obj = EmailOTP.objects.get(user=user)

        if otp_obj.otp == entered_otp:

            login(self.request, user)

            otp_obj.delete()

            messages.success(
                self.request,
                'Login successful.'
            )

            return super().form_valid(form)

        else:

            messages.error(
                self.request,
                'Invalid OTP.'
            )

            return redirect('verify_otp')