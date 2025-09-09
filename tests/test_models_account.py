import uuid
from django.test import TestCase
from django.core.exceptions import ValidationError
from account.models import Account, RecoveryToken, AccountType


class AccountModelTests(TestCase):

    def setUp(self):
        self.account = Account.objects.create(
            username="testuser",
            email=f"user_{uuid.uuid4()}@example.com",
            cpf="12345678901",
            balance=0.00,
            is_active=True,
            is_staff=False,
            type=AccountType.FREE.value
        )

    def test_account_creation(self):
        """Teste a criação de uma conta com dados válidos."""
        self.assertEqual(self.account.type, AccountType.FREE.value)
        self.assertIsNotNone(self.account.id, "Account ID should not be None after saving.")

    def test_account_str_method(self):
        """Teste se o método __str__ retorna a string correta."""
        expected_str = self.account.email
        self.assertEqual(str(self.account), expected_str)


class RecoveryTokenModelTests(TestCase):

    def setUp(self):
        self.account = Account.objects.create(
            username="testuser",
            email=f"user_{uuid.uuid4()}@example.com",
            cpf="12345678901",
            balance=0.00,
            is_active=True,
            is_staff=False,
            type=AccountType.FREE.value
        )
        self.token = RecoveryToken.objects.create(account=self.account)

    def test_recovery_token_creation(self):
        """Teste a criação de um token de recuperação associado a uma conta."""
        self.assertIsNotNone(self.token.id, "Token ID should not be None after saving.")
        self.assertIsNotNone(self.token.value, "Token value should be generated and saved.")

    def test_token_activation(self):
        """Teste a ativação do token."""
        self.token.is_active = False
        self.token.save()
        self.assertFalse(self.token.is_active, "Token should be inactive after being set to False.")

    def test_token_string_representation(self):
        """Teste se o método __str__ retorna a string correta."""
        expected_str = self.token.value
        self.assertEqual(str(self.token), expected_str)
