from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from . models import UserBankAccount,UserAddress

Account_Type=(
    ('Saving Account','Saving Account'),
    ('Current Account','Current Account'),
)
Gender_Type=(
    ('Male','Male'),
    ('Female','Female'),
)
class UserRegistrationForm(UserCreationForm):
    account_type=forms.ChoiceField(choices=Account_Type)
    birth_date=forms.DateField()
    gender=forms.ChoiceField(choices=Gender_Type)

    city=forms.CharField()
    postal_code=forms.CharField()
    country=forms.CharField()  

    class Meta:
        model=User
        fields=['username','password1','password2','email','first_name','last_name','account_type','gender','postal_code','city','country']


    def save(self, commit=True):
     user = super().save(commit=False)
     if commit:
        user.save()

        account_type=self.cleaned_data['account_type']
        birth_date=self.cleaned_data['birth_date']
        gender=self.cleaned_data['gender']
        city=self.cleaned_data['city']
        postal_code=self.cleaned_data['postal_code']
        country=self.cleaned_data['country']

        UserAddress.objects.create(
            user=user,
            city=city,
            postal_code=postal_code,
            country=country,
        )
        UserBankAccount.objects.create(
           user=user,
           account_type=account_type,
           account_no=100000+user.id,
           birth_date=birth_date,
           gender=gender,
        )
        return user
