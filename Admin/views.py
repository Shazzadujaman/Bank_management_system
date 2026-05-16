from pyexpat.errors import messages

from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView, View

from Admin import admin
from accounts.models import UserBankAccount
from transactions.models import Transaction
from .mixins import AdminRequiredMixin
from django.views.generic import ListView
from django.shortcuts import get_object_or_404, redirect

class AdminDashboardView(
    AdminRequiredMixin,
    TemplateView
):

    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context['total_users'] = UserBankAccount.objects.count()

        context['total_transactions'] = Transaction.objects.count()

        context['pending_loans'] = Transaction.objects.filter(
            loan_approve=False,
            transaction_type=3
        ).count()

        context['total_balance'] = sum(
            account.balance
            for account in UserBankAccount.objects.all()
        )

        return context
    





class PendingLoanListView(
    AdminRequiredMixin,
    ListView
):

    model = Transaction

    template_name = 'pending_loans.html'

    context_object_name = 'loans'

    def get_queryset(self):

        return Transaction.objects.filter(
            transaction_type=3,
            loan_approve=False
        )    
    




class ApproveLoanView(AdminRequiredMixin, View):

    def get(self, request, loan_id):

        loan = get_object_or_404(
            Transaction,
            id=loan_id
        )

        loan.loan_approve = True

        loan.save()

        account = loan.account

        account.balance += loan.amount

        account.save()

        messages.success(
            request,
            'Loan approved successfully.'
        )

        return redirect('pending_loans')    
    


class FreezeAccountView(AdminRequiredMixin, View):

    def get(self, request, account_id):

        account = get_object_or_404(
            UserBankAccount,
            id=account_id
        )

        account.is_frozen = not account.is_frozen

        account.save()

        return redirect('manage_users')
    


class ManageUsersView(
    AdminRequiredMixin,
    ListView
):

    model = UserBankAccount

    template_name = 'manage_users.html'

    context_object_name = 'users'



class AllTransactionsView(
    AdminRequiredMixin,
    ListView
):

    model = Transaction

    template_name = 'all_transactions.html'

    context_object_name = 'transactions'

    ordering = ['-timestamp']