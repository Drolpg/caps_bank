import uuid
from django.test import TestCase
from transfers.models import Account, Transaction
from transfers.forms import TransactionForm

class TransactionFormTests(TestCase):

    def setUp(self):
        unique_email1 = f"user1_{uuid.uuid4()}@example.com"
        unique_email2 = f"user2_{uuid.uuid4()}@example.com"

        self.user = Account.objects.create(cpf="12345678901", email=unique_email1, balance=100.00)
        self.other_user = Account.objects.create(cpf="12345678902", email=unique_email2, balance=50.00)

 
        self.user_account = self.user
        self.other_account = self.other_user

        self.form_data = {
            'amount': 10.00,
            'to_account': self.other_account.pk,
            'to_account_cpf': '',
        }

        self.transaction = Transaction.objects.create(
            from_account=self.user_account,
            to_account=self.other_account,
            amount=10.00
        )

        self.form = TransactionForm(user=self.user_account)

    def test_valid_form_with_existing_account(self):
        self.form_data['to_account'] = self.other_account.pk
        form = TransactionForm(data=self.form_data, user=self.user_account)
        self.assertTrue(form.is_valid())

    def test_valid_form_with_new_account(self):
        unique_cpf = f"{uuid.uuid4().int}"[:11]
        self.form_data['to_account_cpf'] = unique_cpf
        Account.objects.create(cpf=self.form_data['to_account_cpf'], email=f"{unique_cpf}@example.com")
        form = TransactionForm(data=self.form_data, user=self.user_account)
        self.assertTrue(form.is_valid())

    def test_invalid_form_both_accounts(self):
        self.form_data['to_account'] = self.other_account.pk
        self.form_data['to_account_cpf'] = "12345678902"

        form = TransactionForm(data=self.form_data, user=self.user_account)
    
        is_valid = form.is_valid()
        print(form.errors)
        self.assertFalse(is_valid)
        self.assertIn('A conta com o CPF fornecido não foi encontrada.', form.errors.get('__all__', []))


    def test_invalid_form_none_selected(self):
        form = TransactionForm(data=self.form_data, user=self.user_account)
        self.assertFalse(form.is_valid())
        self.assertIn('Selecione um contato existente ou insira um novo CPF.', form.errors.get('__all__', []))

    def test_invalid_form_for_own_account(self):
        self.form_data['to_account_cpf'] = self.user_account.cpf
        form = TransactionForm(data=self.form_data, user=self.user_account)
        self.assertFalse(form.is_valid())
        self.assertIn('Você não pode fazer uma transferência para sua própria conta.', form.errors.get('__all__', []))

    def test_invalid_form_with_nonexistent_account(self):
        self.form_data['to_account_cpf'] = "00000000000"
        form = TransactionForm(data=self.form_data, user=self.user_account)
        self.assertFalse(form.is_valid())
        self.assertIn('A conta com o CPF fornecido não foi encontrada.', form.errors.get('__all__', []))
