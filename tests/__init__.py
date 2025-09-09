from transfers.models import Account, Transaction
from transfers.forms import TransactionForm

def __init__(self, *args, user=None, **kwargs):
    super(TransactionForm, self).__init__(*args, **kwargs)
    self.user = user
    if user:
        to_accounts_cpf = Transaction.objects.filter(from_account=user).values_list("to_account", flat=True)
        to_accounts = Account.objects.filter(cpf__in=to_accounts_cpf)
        self.fields["to_account"].queryset = to_accounts

        print("Queryset for to_account:", self.fields["to_account"].queryset)
