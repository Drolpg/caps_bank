import uuid
from django.test import TestCase
from account.models import Account, RecoveryToken
from account.forms import (
    RecoveryPasswordRequestForm,
    RecoveryPasswordConfirmForm,
    LoginForm,
    AccountRegistrationForm,
)


class RecoveryPasswordRequestFormTests(TestCase):

    def test_valid_email(self):
        email = f"user_{uuid.uuid4()}@example.com"
        Account.objects.create(email=email)
        form = RecoveryPasswordRequestForm(data={'email': email})
        self.assertTrue(form.is_valid())

    def test_invalid_email(self):
        form = RecoveryPasswordRequestForm(data={'email': 'invalid@example.com'})
        self.assertFalse(form.is_valid())
        self.assertIn('Não há nenhuma conta com esse email, por favor, verifique o email novamente.', form.errors['__all__'])


class RecoveryPasswordConfirmFormTests(TestCase):

    def setUp(self):
        self.valid_email = f"user_{uuid.uuid4()}@example.com"
        self.token = "valid_token"
        self.account = Account.objects.create(email=self.valid_email)
        self.recovery_token = RecoveryToken.objects.create(value=self.token, account=self.account)

    def test_valid_token_and_passwords_match(self):
        form = RecoveryPasswordConfirmForm(data={
            'token': self.token,
            'password': 'newpassword123',
            'confirm_password': 'newpassword123',
        })
        self.assertTrue(form.is_valid())

    def test_passwords_do_not_match(self):
        form = RecoveryPasswordConfirmForm(data={
            'token': self.token,
            'password': 'newpassword123',
            'confirm_password': 'differentpassword',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('As senhas não coincidem.', form.errors['__all__'])

    def test_invalid_token(self):
        form = RecoveryPasswordConfirmForm(data={
            'token': 'invalid_token',
            'password': 'newpassword123',
            'confirm_password': 'newpassword123',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('Código informado não existe ou expirou.', form.errors['__all__'])


class LoginFormTests(TestCase):

    def setUp(self):
        self.valid_email = f"user_{uuid.uuid4()}@example.com"
        self.password = 'password123'
        self.account = Account.objects.create(email=self.valid_email)
        self.account.set_password(self.password)
        self.account.save()

    def test_login_form_invalid_email(self):
        form = LoginForm(data={'email': 'invalid_email@example.com', 'password': 'password123'})
        self.assertFalse(form.is_valid(), msg=form.errors)
        self.assertIn('Endereço de e-mail inválido.', form.errors['email'])

    def test_login_form_invalid_password(self):
        form = LoginForm(data={'email': self.valid_email, 'password': 'wrongpassword'})
        self.assertFalse(form.is_valid(), msg=form.errors)
        self.assertIn('Senha inválida.', form.errors['password'])

    def test_valid_login_form(self):
        form = LoginForm(data={'email': self.valid_email, 'password': self.password})
        self.assertTrue(form.is_valid())


class AccountRegistrationFormTests(TestCase):

    def setUp(self):
        self.valid_cpf = '30995030022'

    def test_valid_registration_form(self):
        form = AccountRegistrationForm(data={
            'username': 'testuser',
            'email': f"user_{uuid.uuid4()}@example.com",
            'cpf': self.valid_cpf,
            'password': 'password123',
            'confirm_password': 'password123',
        })
        self.assertTrue(form.is_valid(), msg=form.errors)

    def test_invalid_email(self):
        form = AccountRegistrationForm(data={
            'username': 'testuser',
            'email': 'invalid_email',
            'cpf': self.valid_cpf,
            'password': 'password123',
            'confirm_password': 'password123',
        })
        self.assertFalse(form.is_valid(), msg=form.errors)
        self.assertIn('Endereço de e-mail invalido.', form.errors['email'])

    def test_passwords_do_not_match(self):
        form = AccountRegistrationForm(data={
            'username': 'testuser',
            'email': f"user_{uuid.uuid4()}@example.com",
            'cpf': self.valid_cpf,
            'password': 'password123',
            'confirm_password': 'differentpassword',
        })
        self.assertFalse(form.is_valid(), msg=form.errors)
        self.assertIn('As senhas não coincidem.', form.errors['__all__'])
