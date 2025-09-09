from enum import Enum
from random import randint
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from .managers import AccountManager


class AccountType(Enum):
    FREE = "free"
    PREMIUM = "premium"
    ADMIN = "admin"

    @classmethod
    def choices(cls):
        return [(item.value, item.name.capitalize()) for item in cls]


class Account(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=100, verbose_name="nome de usuário")
    email = models.EmailField(max_length=100, unique=True)
    cpf = models.CharField(max_length=11, unique=True, verbose_name="CPF")
    balance = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.0, verbose_name="saldo"
    )
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    type = models.CharField(
        max_length=10,
        choices=AccountType.choices(),
        default=AccountType.FREE.value,
        verbose_name="tipo de conta",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["cpf", "username"]

    objects = AccountManager()

    def __str__(self):
        return self.email


class Deposit(models.Model):
    to_account = models.ForeignKey(
        Account, related_name="deposit", on_delete=models.CASCADE
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Depósito para {self.to_account} no valor de R${self.amount} em {self.timestamp}"


class RecoveryToken(models.Model):
    value = models.CharField(max_length=9, unique=True)
    is_active = models.BooleanField(default=True)
    account = models.ForeignKey(Account, related_name="token", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    @classmethod
    def generate_numeric_token(cls):
        return str(randint(100000000, 999999999))

    def save(self, *args, **kwargs):
        if not self.value:
            self.value = self.generate_unique_numeric_token()
        super().save(*args, **kwargs)

    def generate_unique_numeric_token(self):
        token = self.generate_numeric_token()
        while RecoveryToken.objects.filter(value=token).exists():
            token = self.generate_numeric_token()

        return token


class Flag(models.Model):
    name = models.CharField(max_length=100, verbose_name="nome", unique=True)
    active = models.BooleanField(default=False, verbose_name="ativo")
