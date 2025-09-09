# investments/forms.py
from django import forms
from .models import Investment


class InvestmentForm(forms.ModelForm):
    class Meta:
        model = Investment
        fields = ["applied_value"]
        labels = {"applied_value": "Valor do Investimento"}
