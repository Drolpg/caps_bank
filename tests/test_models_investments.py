from django.test import TestCase
from investments.models import Indexer, ProductInvestment, Investment
from account.models import Account
from decimal import Decimal
from django.utils import timezone

class IndexerModelTest(TestCase):
    def test_str_method(self):
        indexer = Indexer.objects.create(name="Test Indexer", rate=Decimal('1.50'))
        self.assertEqual(str(indexer), "Test Indexer")


class ProductInvestmentModelTest(TestCase):
    def setUp(self):
        self.indexer = Indexer.objects.create(name="Test Indexer", rate=Decimal('1.50'))
        self.product = ProductInvestment.objects.create(
            name="Test Product",
            tax=Decimal('2.00'),
            index_multiplier=Decimal('1.00'),
            indexer=self.indexer,
            final_date=timezone.now() + timezone.timedelta(days=30),
            minimum_value=Decimal('100.00')
        )

    def test_str_method(self):
        self.assertEqual(str(self.product), "Test Product")

    def test_get_daily_tax(self):
        expected_tax = (Decimal('2.00') + (Decimal('1.50') * Decimal('1.00'))) / 365 / 100
        self.assertAlmostEqual(self.product.get_daily_tax(), expected_tax)

    def test_get_monthly_tax(self):
        expected_tax = round((Decimal('2.00') + (Decimal('1.50') * Decimal('1.00'))), 2)
        self.assertEqual(self.product.get_monthly_tax(), expected_tax)


class InvestmentModelTest(TestCase):
    def setUp(self):
        self.account = Account.objects.create(
            username='testuser',
            password='password',
            email='test@example.com',
        )
        self.indexer = Indexer.objects.create(name="Test Indexer", rate=Decimal('1.50'))
        self.product = ProductInvestment.objects.create(
            name="Test Product",
            tax=Decimal('2.00'),
            index_multiplier=Decimal('1.00'),
            indexer=self.indexer,
            final_date=timezone.now() + timezone.timedelta(days=30),
            minimum_value=Decimal('100.00')
        )
        self.investment = Investment.objects.create(
            account=self.account,
            product=self.product,
            applied_value=Decimal('500.00')
        )

    def test_str_method(self):
        self.assertEqual(str(self.investment), f"Investimento de {self.account} no produto Test Product")

    def test_update_income(self):
        initial_income = self.investment.accumulated_income
        self.investment.update_income()
        self.assertGreater(self.investment.accumulated_income, initial_income)

    def test_rescue_investment(self):
        total_amount = self.investment.rescue_investment()
        self.assertEqual(total_amount, self.investment.applied_value + self.investment.accumulated_income)
        self.assertEqual(self.investment.status, 'resgatado')
        self.assertIsNotNone(self.investment.rescue_date)

    def test_rescue_investment_not_active(self):
        self.investment.status = 'resgatado'
        with self.assertRaises(ValueError):
            self.investment.rescue_investment()
