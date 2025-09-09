import uuid
from django.test import TestCase
from django.core.exceptions import ValidationError
from account.models import Account
from transfers.models import Transaction

class TransactionModelTests(TestCase):

    def setUp(self):
        self.sender_account = Account.objects.create(
            cpf="12345678901",
            email=f"sender_{uuid.uuid4()}@example1.com",
            balance=100.00
        )
        self.receiver_account = Account.objects.create(
            cpf="12345678902",
            email=f"receiver_{uuid.uuid4()}@example2.com",
            balance=50.00
        )

    def test_transaction_creation(self):
        """Teste a criação de uma transação com dados válidos."""
        transaction = Transaction.objects.create(
            from_account=self.sender_account,
            to_account=self.receiver_account,
            amount=10.00,
            token='123456'
        )
        self.assertEqual(transaction.from_account, self.sender_account)
        self.assertEqual(transaction.to_account, self.receiver_account)
        self.assertEqual(transaction.amount, 10.00)
        self.assertEqual(transaction.token, '123456')
        self.assertFalse(transaction.is_committed)

    def test_transaction_str_method(self):
        """Teste se o método __str__ retorna a string correta."""
        transaction = Transaction.objects.create(
            from_account=self.sender_account,
            to_account=self.receiver_account,
            amount=10.00,
            token='123456'
        )
        expected_str = f"Transferência de {self.sender_account} para {self.receiver_account} no valor de R${transaction.amount:.2f} em {transaction.timestamp}"
        self.assertEqual(str(transaction), expected_str)

    def test_transaction_amount_validation(self):
        """Teste se a quantidade não pode ser negativa."""
        transaction = Transaction(
            from_account=self.sender_account,
            to_account=self.receiver_account,
            amount=-10.00,
            token='123456'
        )
        with self.assertRaises(ValidationError):
            transaction.full_clean()
