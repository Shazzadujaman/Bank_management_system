from django.urls import path,include

from . import views
from .views import PendingLoanListView, ApproveLoanView, ManageUsersView, FreezeAccountView,AllTransactionsView, AdminDashboardView, AdminRequiredMixin
urlpatterns=[
    path(
    'admin-dashboard/',
    views.AdminDashboardView.as_view(),
    name='admin_dashboard'
),

path(
    'pending-loans/',
    views.PendingLoanListView.as_view(),
    name='pending_loans'
),

path(
    'approve-loan/<int:loan_id>/',
    views.ApproveLoanView.as_view(),
    name='approve_loan'
),

path(
    'manage-users/',
    views.ManageUsersView.as_view(),
    name='manage_users'
),

path(
    'freeze-account/<int:account_id>/',
    views.FreezeAccountView.as_view(),
    name='freeze_account'
),

path(
    'all-transactions/',
    views.AllTransactionsView.as_view(),
    name='all_transactions'
),
]