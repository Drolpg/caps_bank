from django.test import TestCase
from decimal import Decimal
from django.urls import reverse
from django.utils import timezone
from account.models import Account
from transfers.models import Transaction
from django.contrib.auth import get_user_model
from unittest.mock import patch

User = get_user_model()

class TransactionViewsTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='password',
            email='userty@example.com',
            cpf='12345678901'
        )
        self.other_user = User.objects.create_user(
            username='testuser2',
            password='password',
            email='otherty@example.com',
            cpf='38244094028'
        )

        self.user_account = Account.objects.create(
            balance=100.00,
            cpf='38244094028',
            email='userty@example.com',
            username='testuser',
        )
        self.other_account = Account.objects.create(
            balance=50.00,
            cpf='83803998034',
            email='otherty@example.com',
            username='testuser2',
        )

        self.assertIsNotNone(self.user.pk, "Usuário testuser não foi criado corretamente.")
        self.assertIsNotNone(self.other_user.pk, "Usuário testuser2 não foi criado corretamente.")

        self.login_user()

    def login_user(self):
        login_success = self.client.login(username='testuser', password='password')
        self.assertTrue(login_success, "Falha ao fazer login com o usuário de teste.")

    def test_transaction_view_valid_post(self):
        response = self.client.post(reverse('transaction'), {
            'amount': 10.00,
            'to_account': self.other_account.id,
        })
        self.assertRedirects(response, reverse('confirm_transaction'))

        transaction_token = self.client.session.get("transaction_token")
        self.assertIsNotNone(transaction_token, "Token de transação não foi definido na sessão.")

    def test_transaction_view_insufficient_balance(self):
        self.user_account.balance = Decimal('5.00')
        self.user_account.save()

        response = self.client.post(reverse('transaction'), {
            'amount': 10.00,
            'to_account': self.other_account.id,
        })
        self.assertRedirects(response, reverse('home'))
        self.assertContains(response, "Saldo insuficiente para realizar a transação.")

    def test_confirm_transaction_view_valid_post(self):
        self.client.post(reverse('transaction'), {
            'amount': 10.00,
            'to_account': self.other_account.id,
        })

        transaction_token = self.client.session.get("transaction_token")
        self.assertIsNotNone(transaction_token, "Token de transação não foi definido na sessão.")

        response = self.client.post(reverse('confirm_transaction'), {
            'token': transaction_token,
        })

        self.assertRedirects(response, reverse('home'))
        self.assertContains(response, "Transação confirmada com sucesso!")
        self.assertEqual(Transaction.objects.count(), 1)

    def test_confirm_transaction_view_invalid_token(self):
        self.client.post(reverse('transaction'), {
            'amount': 10.00,
            'to_account': self.other_account.id,
        })

        transaction_token = self.client.session.get("transaction_token")

        response = self.client.post(reverse('confirm_transaction'), {
            'token': 'invalid_token',
        })

        self.assertTemplateUsed(response, 'confirm_transaction.html')
        self.assertContains(response, "Token inválido. Verifique o token e tente novamente.")

    def test_confirm_transaction_view_expired_token(self):
        self.client.post(reverse('transaction'), {
            'amount': 10.00,
            'to_account': self.other_account.id,
        })

        transaction_token = self.client.session.get("transaction_token")
        self.assertIsNotNone(transaction_token, "Token de transação não foi definido na sessão.")

        self.client.session['token_expiration'] = (timezone.now() - timezone.timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S")

        response = self.client.post(reverse('confirm_transaction'), {
            'token': transaction_token,
        })

        self.assertTemplateUsed(response, 'confirm_transaction.html')
        self.assertContains(response, "O token expirou. Solicite uma nova transação.")

    @patch('transfers.views.celery_send_mail')
    def test_email_sent_on_transaction(self, mock_send_mail):
        response = self.client.post(reverse('transaction'), {
            'amount': 10.00,
            'to_account': self.other_account.id,
        })

        self.assertRedirects(response, reverse('confirm_transaction'))

        self.assertTrue(mock_send_mail.called)

        args, kwargs = mock_send_mail.call_args[0]
        self.assertIn('Token da transação', args[0])
        self.assertIn('Seu token é', args[1])