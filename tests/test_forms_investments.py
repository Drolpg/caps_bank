from django.test import TestCase
from investments.forms import InvestmentForm
from decimal import Decimal

class InvestmentFormTest(TestCase):
    def test_investment_form_valid(self):
        form_data = {
            'applied_value': Decimal('500.00')
        }
        form = InvestmentForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['applied_value'], Decimal('500.00'))

    def test_investment_form_invalid(self):
        form_data = {
            'applied_value': '' 
        }
        form = InvestmentForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('applied_value', form.errors)
        
    