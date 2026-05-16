from django.urls import path

from . import views
urlpatterns=[
    path(
    'currency-converter/',
    views.CurrencyConvertView.as_view(),
    name='currency_converter'
),
]
