from django.test import TestCase
from django.urls import reverse
from account.models import Account

class AccountViewsTests(TestCase):

    def setUp(self):
        self.user_data = {
            'username': 'testuser',
            'email': 'squadtech.capsbank@gmail.com',
            'cpf': '11500634670',
            'password': 'qhzsjfsozztpveya',
            'confirm_password': 'qhzsjfsozztpveya',
        }

    def test_register_view(self):
        response = self.client.post(reverse('register'), self.user_data)
        print("Status code após registro:", response.status_code)
        self.assertEqual(response.status_code, 302)
        
        account_exists = Account.objects.filter(email=self.user_data['email']).exists()
        print("Account exists:", account_exists)
        self.assertTrue(account_exists)

    def test_login_view(self):
        self.client.post(reverse('register'), self.user_data)
        response = self.client.post(reverse('login'), {
            'email': self.user_data['email'],
            'password': self.user_data['password'],
        })
        print("Status code após login:", response.status_code)
        self.assertEqual(response.status_code, 302)
        
    def test_home_view(self):
        self.client.post(reverse('register'), self.user_data)

        self.client.login(email=self.user_data['email'], password=self.user_data['password'])
        response = self.client.get(reverse('home'))
        
        print("Status code após acessar home:", response.status_code)
        self.assertEqual(response.status_code, 200)

    def test_confirm_view(self):
        self.client.post(reverse('register'), self.user_data)

    def test_recovery_password_view(self):
        self.client.post(reverse('register'), self.user_data)
        response = self.client.get(reverse('password-recovery'))
        self.assertEqual(response.status_code, 200)
