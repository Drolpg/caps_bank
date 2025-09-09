from django.urls import path
from .views import TransactionView , ConfirmTransactionView

urlpatterns = [
    path('transaction/', TransactionView.as_view(), name='transaction'),
    path('confirm-transaction/', ConfirmTransactionView.as_view(), name='confirm_transaction')
]