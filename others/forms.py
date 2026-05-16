from django import forms


CURRENCY_CHOICES = [

    ('USD', 'US Dollar'),
    ('BDT', 'Bangladeshi Taka'),
    ('EUR', 'Euro'),
    ('INR', 'Indian Rupee'),

]


class CurrencyConvertForm(forms.Form):

    amount = forms.FloatField()

    from_currency = forms.ChoiceField(
        choices=CURRENCY_CHOICES
    )

    to_currency = forms.ChoiceField(
        choices=CURRENCY_CHOICES
    )