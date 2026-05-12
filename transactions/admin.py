from django.contrib import admin

from transactions.utils import send_transaction_email

# Register your models here.
from .models import Transaction

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display=['account','amount','balance_after_transaction','transaction_type','loan_approve']

    def save_model(self, request, obj, form, change):
        if obj.loan_approve==True:
            obj.account.balance+=obj.amount
            obj.balance_after_transaction=obj.account.balance
            obj.account.save()

            send_transaction_email(obj.account.user, obj.amount, 'loan approved')
            super().save_model(request, obj, form, change)