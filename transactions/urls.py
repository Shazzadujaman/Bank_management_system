from django.urls import path
from .views import PayLoanView,LoanListView, DepositView, TransferMoneyView,WithdrawView,LoanRequestView,TransactionReportView
urlpatterns=[
    path('deposit/',DepositView.as_view(),name='deposit'),
    path('withdraw/',WithdrawView.as_view(),name='withdraw'),
    path('loan-request/',LoanRequestView.as_view(),name='loan_request'),
    path('pay-loan/<int:pk>/',PayLoanView.as_view(),name='pay_loan'),
    path('loans/',LoanListView.as_view(),name='loans'),
    path('report/',TransactionReportView.as_view(),name='transaction_report'),
    path('loan-list/',LoanListView.as_view(),name='loan_list'),
    path('pay-loan/<int:loan_id>/',PayLoanView.as_view(),name='pay_loan'),
    path('transfer/',TransferMoneyView.as_view(),name='transfer'),
]
