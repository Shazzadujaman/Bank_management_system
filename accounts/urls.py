from django.urls import path,include
from . import views

urlpatterns = [
    path('registration/',views.UserRegistrationView.as_view(),name='registrations'),
    path('login/',views.UserLoginView.as_view(),name='login'),
    path('logout/',views.UserLogoutView.as_view(),name='logout'),
]
