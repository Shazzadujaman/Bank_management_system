from django.shortcuts import render

# Create your views here.
import requests

from django.views.generic.edit import FormView


from .forms import CurrencyConvertForm


class CurrencyConvertView(FormView):

    template_name = 'currency_converter.html'

    form_class = CurrencyConvertForm


    def form_valid(self, form):

        amount = form.cleaned_data['amount']

        from_currency = form.cleaned_data['from_currency']

        to_currency = form.cleaned_data['to_currency']

        url = f'https://api.exchangerate-api.com/v4/latest/{from_currency}'

        response = requests.get(url)

        data = response.json()

        rate = data['rates'][to_currency]

        converted_amount = amount * rate

        return render(
            self.request,
            self.template_name,
            {
                'form': form,
                'converted_amount': round(converted_amount, 2),
                'rate': rate
            }
        )