from django import forms
from django.core.exceptions import ValidationError
from .models import Account, Transaction


class TransactionForm(forms.Form):
    to_account = forms.ModelChoiceField(
        label="Selecione o contato",
        queryset=Account.objects.none(),
        empty_label="Selecione o contato de destino",
        to_field_name="cpf",
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    to_account_cpf = forms.CharField(
        label="Novo contato",
        max_length=11,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Digite o CPF do novo contato', "data-mask": "000.000.000-00", "data-mask-selectonfocus": "true"}),
    )

    amount = forms.DecimalField(
        label="Valor da Transferência",
        max_digits=10,
        decimal_places=2,
        required=True,
        widget=forms.NumberInput(
        attrs={"class": "form-control","placeholder": "Insira o valor da transferência"}
        ),
    )

    def __init__(self, *args, user=None, **kwargs):
        super(TransactionForm, self).__init__(*args, **kwargs)
        self.user = user
        if user:
            to_accounts_cpf = Transaction.objects.filter(from_account=user).values_list(
                "to_account", flat=True
            )
            to_accounts = Account.objects.filter(cpf__in=to_accounts_cpf)
            self.fields["to_account"].queryset = to_accounts

    def clean(self):
        cleaned_data = super().clean()
        to_account = cleaned_data.get("to_account")
        to_account_cpf = cleaned_data.get("to_account_cpf")

        if to_account and to_account_cpf:
            raise ValidationError("Você só pode selecionar uma opção de conta de destino: escolha entre a conta existente ou insira um novo CPF.")

        if not to_account and not to_account_cpf:
            raise ValidationError("Selecione um contato existente ou insira um novo CPF.")

        if to_account_cpf:
            if not Account.objects.filter(cpf=to_account_cpf).exists():
                raise ValidationError("A conta com o CPF fornecido não foi encontrada.")

            to_account = Account.objects.get(cpf=to_account_cpf)
            cleaned_data['to_account'] = to_account
        
        if to_account_cpf == self.user.cpf:
            raise ValidationError("Você não pode fazer uma transferência para sua própria conta.")

        return cleaned_data
