from django.db import models
from django.contrib.auth.models import User

# Create your models here.
Account_Type=(
    ('Saving Account','Saving Account'),
    ('Current Account','Current Account'),
)
Gender_Type=(
    ('Male','Male'),
    ('Female','Female'),
)
class UserBankAccount(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='account')
    account_type=models.CharField(choices=Account_Type)
    account_no=models.IntegerField(unique=True)
    birth_date=models.DateField()
    gender=models.CharField(choices=Gender_Type)
    initial_deposit_date=models.DateField(auto_now_add=True)
    balance=models.DecimalField(default=0.00,max_digits=10,decimal_places=2)

    def __str__(self):
        return self.user.username

class UserAddress(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='address')
    city=models.CharField()
    postal_code=models.CharField()
    country=models.CharField()  

    def __str__(self):
        return self.user.email  
