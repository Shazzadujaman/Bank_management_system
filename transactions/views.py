from urllib import request

from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

from others.utils import create_notification
from transactions.utils import send_transaction_email
from .models import Transaction
from .forms import DepositForm,WithdrawForm,LoanRequstForm
from django.contrib import messages
from django.utils.dateparse import parse_date
from django.views.generic import ListView
from django.views import View
from django.shortcuts import get_object_or_404, redirect
from  .constants import TRANSACTION_TYPES
from .forms import TransferForm
from accounts.models import UserBankAccount
from django.db import transaction
from django.views.generic import FormView


class TransactionCreateMixin(LoginRequiredMixin,CreateView):
    model=Transaction
    template_name='transaction_form.html'
    title='Transaction'
    success_url=reverse_lazy('transaction_report')

    def get_form_kwargs(self):
        kwargs=super().get_form_kwargs()
        kwargs.update({
            'account':self.request.user.account,
        })
        return kwargs
    
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context.update({
            'title':self.title
        })
        return context


class DepositView(TransactionCreateMixin):
    form_class=DepositForm    
    title="Deposit"

    def get_initial(self):
        initial={'transaction_type':1}
        return initial
    
    def form_valid(self, form):
        
        amount=form.cleaned_data.get('amount')
        account=self.request.user.account

        if account.is_frozen:

            messages.error(
               self.request,
               'Your account is frozen.'
            )

            return redirect('home') 
        account.balance+=amount
        account.save(
            update_fields=['balance']
        )
        send_transaction_email(
           self.request.user,
           amount,
          'Deposit'
       )  
        create_notification(
        self.request.user,
        f'{amount} BDT deposited successfully.'
       )

        messages.success(self.request,f"{amount}$ was deposited to your account successfully")
        return super().form_valid(form)
        
    
    


class WithdrawView(TransactionCreateMixin):
    form_class=WithdrawForm    
    title="Withdraw"

    def get_initial(self):
        initial={'transaction_type': 2}
        return initial
    
    def form_valid(self, form):
        
        amount=form.cleaned_data.get('amount')
        account=self.request.user.account
        if account.is_frozen:

           messages.error(
           self.request,
           'Your account is frozen.'
           ) 

           return redirect('home')
        account.balance-=amount
        account.save(
            update_fields=['balance']
        )

        send_transaction_email(
            self.request.user,
            amount,
            'Withdraw'
        )

        messages.success(self.request,f"{amount}$ was withdrawn from your account successfully")
        return super().form_valid(form)  
   


class LoanRequestView(TransactionCreateMixin):
    form_class=LoanRequstForm    
    title="Loan Request"
    

    def get_initial(self):
        initial={'transaction_type': 3}
        return initial
    
    def form_valid(self, form):
        amount=form.cleaned_data.get('amount')
        current_loan_count=Transaction.objects.filter(account=self.request.user.account,transaction_type=3,loan_approve=True).count()
        if current_loan_count>=3:
            return HttpResponse("You have crossed your limits")
        messages.success(self.request,f"loan request of {amount}$ was sent successfully, wait for the approval")
        send_transaction_email(self.request.user, amount, 'loan request')
        return super().form_valid(form)      
    

class TransactionReportView(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = 'transaction_report.html'
    context_object_name = 'transactions'
    paginate_by = 10

    def get_queryset(self):
        # logged-in user account
        account = self.request.user.account

        queryset = Transaction.objects.filter(account=account)

        # date filtering
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')

        if start_date and end_date:
            start_date = parse_date(start_date)
            end_date = parse_date(end_date)

            if start_date and end_date:
                queryset = queryset.filter(
                    timestamp__date__gte=start_date,
                    timestamp__date__lte=end_date
                )

        return queryset.order_by('-timestamp')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            'title': 'Transaction Report',
            'start_date': self.request.GET.get('start_date'),
            'end_date': self.request.GET.get('end_date'),
        })

        return context
    
class PayLoanView(LoginRequiredMixin, View):
    def get(self, request, pk):

        loan = get_object_or_404(Transaction, id=pk)
        user_account = request.user.account

        # 🔒 Security check
        if loan.account != user_account:
            messages.error(request, "Unauthorized access!")
            return redirect("loan_list")

        # Already paid check
        if loan.amount <= 0:
            messages.info(request, "This loan is already paid.")
            return redirect("loan_list")

        # 💰 Check balance
        if user_account.balance >= loan.amount:

            # Deduct balance
            user_account.balance -= loan.amount
            user_account.save()

            # Mark loan as paid
            loan.amount = 0
            loan.balance_after_transaction = user_account.balance
            loan.save()

            messages.success(request, "Loan paid successfully ✅")

        else:
            messages.error(request, "Insufficient balance ❌")

        return redirect("loan_list")
    


class LoanListView(LoginRequiredMixin,ListView):
    model=Transaction
    template_name="loanlist.html"
    context_object_name="loans"

    def get_queryset(self):
        user_account=self.request.user.account
        queryset=Transaction.objects.filter(account=user_account, transaction_type=3)
        return queryset


class TransferMoneyView(LoginRequiredMixin, FormView):

    template_name = 'transfer.html'
    form_class = TransferForm
    success_url = reverse_lazy('home')

    @transaction.atomic
    def form_valid(self, form):

        receiver_account_no = form.cleaned_data['account_no']
        amount = form.cleaned_data['amount']

        sender_account = UserBankAccount.objects.get(
            user=self.request.user
        )

        # ❌ Self transfer check
        if sender_account.account_no == receiver_account_no:
            messages.error(
                self.request,
                "You cannot transfer money to yourself."
            )
            return redirect('transfer')

        # ❌ Balance check
        if sender_account.balance < amount:
            messages.error(
                self.request,
                "Insufficient balance."
            )
            return redirect('transfer')

        # ❌ Receiver check
        try:
            receiver_account = UserBankAccount.objects.get(
                account_no=receiver_account_no
            )

        except UserBankAccount.DoesNotExist:
            messages.error(
                self.request,
                "Receiver account not found."
            )
            return redirect('transfer')

        # ✅ Transfer
        sender_account.balance -= amount
        receiver_account.balance += amount

        sender_account.save()
        receiver_account.save()

        # ✅ Sender transaction
        Transaction.objects.create(
            account=sender_account,
            amount=amount,
            balance_after_transaction=sender_account.balance,
            transaction_type=5
        )

        # ✅ Receiver transaction
        Transaction.objects.create(
            account=receiver_account,
            amount=amount,
            balance_after_transaction=receiver_account.balance,
            transaction_type=6
        )

        messages.success(
            self.request,
            "Money transferred successfully."
        )

        create_notification(
        sender_account.user,
        f'{amount} BDT transferred successfully.'
        )
    
        create_notification(
        receiver_account.user,
        f'You received {amount} BDT.'
        )  
        
        return super().form_valid(form)





        
