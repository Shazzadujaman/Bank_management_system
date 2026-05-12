from django import forms
from .models import Transaction

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['amount', 'transaction_type']



    def __init__(self, *args, **kwargs):
        self.account=kwargs.pop('account')
        super().__init__(*args, **kwargs)
        self.fields['transaction_type'].disabled=True
        self.fields['transaction_type'].widget=forms.HiddenInput()

    def save(self, commit=True):
        self.instance.account=self.account
        self.instance.balance_after_transaction=self.account.balance 
        return super().save(commit=commit)  


class DepositForm(TransactionForm):
    def clean_amount(self):
        min_deposit_amount=100
        amount=self.cleaned_data.get('amount')
        if amount<min_deposit_amount:
            raise forms.ValidationError(
                f'You need to deposit at Least {min_deposit_amount} $'
            )
        
        return amount

    
class WithdrawForm(TransactionForm):
    def clean_amount(self):
        account=self.account
        min_withdraw_amount=500
        max_withdraw_amount=20000
        amount=self.cleaned_data.get('amount')
        balance=account.balance

        if amount<min_withdraw_amount:
            raise forms.ValidationError(
                f'You need to withdraw at least {min_withdraw_amount} $'
            )
        if amount>max_withdraw_amount:
            raise forms.ValidationError(
                f'You can not withdraw more than {max_withdraw_amount} $'
            )
        if amount>balance:
            raise forms.ValidationError(
                'You do not have enough balance to make this transaction'
            )
        return amount
    

class LoanRequstForm(TransactionForm):
    def clean_amount(self):
        account=self.account
        min_loan_amount=1000
        max_loan_amount=50000
        amount=self.cleaned_data.get('amount')
        balance=account.balance

        if amount<min_loan_amount:
            raise forms.ValidationError(
                f'You need to request at least {min_loan_amount} $'
            )
        if amount>max_loan_amount:
            raise forms.ValidationError(
                f'You can not request more than {max_loan_amount} $'
            )
        
        return amount 
    


class TransferForm(forms.Form):
    account_no = forms.IntegerField(
        label='Receiver Account Number'
    )

    amount = forms.DecimalField(
        max_digits=10,
        decimal_places=2
    )
