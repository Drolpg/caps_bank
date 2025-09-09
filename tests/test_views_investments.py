# investments/tests/test_views_investments.py
from django.test import TestCase
from django.urls import reverse
from account.models import Account, AccountType
from investments.models import ProductInvestment, Investment, Indexer
from investments.forms import InvestmentForm


class InvestmentViewsTest(TestCase):

    def setUp(self):
        self.user = Account.objects.create_user(
            username='testuser',
            email='testuser+re@example.com',
            cpf='54392576086',
            password='password'
        )
        self.user.balance = 500.00
        self.user.type = AccountType.NORMAL.value
        self.user.save()

        self.indexer = Indexer.objects.create(name='Test Indexer', rate=1.5)
        self.product = ProductInvestment.objects.create(
            name='Test Product',
            tax=2.0,
            index_multiplier=1,
            indexer=self.indexer,
            final_date='2025-01-01',
            minimum_value=100.00,
            is_premium=False
        )

    def test_product_list_view(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('product_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'product_list.html')
        self.assertContains(response, 'Test Product')

    def test_product_detail_view(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('product_detail', kwargs={'product_id': self.product.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'product_detail.html')
        self.assertContains(response, 'Test Product')

    def test_my_investments_list_view(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('my_investments'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'my_investments.html')

    