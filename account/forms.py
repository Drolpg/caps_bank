from django import forms
from django.core.exceptions import ValidationError
from account.models import Account, RecoveryToken
from account.validations.registration_validations import (
    validate_cpf,
    validate_email,
    validate_password,
    validate_username,
)


class RecoveryPasswordRequestForm(forms.Form):
    email = forms.EmailField(
        max_length=150,
        label="Email",
        widget=forms.EmailInput(attrs={"class": "form-control"}),
    )

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        if not Account.objects.filter(email=email).exists():
            raise ValidationError(
                "Não há nenhuma conta com esse email, por favor, verifique o email novamente.",
            )

        return cleaned_data


class RecoveryPasswordConfirmForm(forms.Form):
    token = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"}), label="Senha"
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        label="Confirmar Senha",
    )

    def clean(self):
        cleaned_data = super().clean()
        token = cleaned_data.get("token")
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        validate_password(password, confirm_password)

        if not RecoveryToken.objects.filter(value=token):
            raise ValidationError("Código informado não existe ou expirou.")

        return cleaned_data


class LoginForm(forms.ModelForm):
    email = forms.EmailField(max_length=150, label="Email", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label="Senha")

    class Meta:
        model = Account
        fields = ["email", "password"]

    def clean(self):
        return self.data


class AccountRegistrationForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),)
    email = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),)
    cpf = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', "data-mask": "000.000.000-00", "data-mask-selectonfocus": "true"},),max_length=11)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label="Senha")
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label="Senha")

    class Meta:
        model = Account
        fields = ["username", "email", "cpf", "password", "confirm_password"]
        labels = {
            "username": "Nome",
            "email": "E-mail",
            "cpf": "CPF",
        }
        error_messages = {
            "username": {
                "required": 'O campo "Nome" é obrigatório.',
            }
        }

    def clean_cpf(self):
        cpf = self.cleaned_data.get("cpf")
        validate_cpf(cpf)
        return cpf

    def clean_username(self):
        username = self.cleaned_data.get("username")
        validate_username(username)
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        validate_email(email)
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        validate_password(password, confirm_password)

        return cleaned_data
