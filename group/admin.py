from django import forms
from django.contrib import admin
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _

from account.models import Deposit

from .models import Group


class BalanceForm(forms.Form):
    amount = forms.DecimalField(
        label="Valor a ser adicionado", max_digits=10, decimal_places=2
    )


class GroupAdmin(admin.ModelAdmin):
    list_display = ("name", "begin", "end")
    search_fields = ("name",)
    fieldsets = (
        ("Informações da turma", {"fields": ["name", "icon"]}),
        (
            "Datas",
            {
                "fields": [
                    ("begin", "end"),
                ]
            },
        ),
        (
            "Participantes",
            {
                "fields": [
                    "accounts",
                ]
            },
        ),
    )
    filter_horizontal = ("accounts",)

    actions = ["add_balance_to_accounts"]

    def add_balance_to_accounts(self, request, queryset):
        if "apply" in request.POST:
            form = BalanceForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data["amount"]
                for group in queryset:
                    accounts = group.accounts.all()
                    for account in accounts:
                        account.balance += amount
                        deposit = Deposit.objects.create(
                            to_account=account, amount=amount
                        )
                        account.save()
                return None

        else:
            form = BalanceForm()

        return render(
            request,
            "admin/add_balance_group.html",
            {
                "form": form,
                "queryset": queryset,
                "action_checkbox_name": admin.helpers.ACTION_CHECKBOX_NAME,
            },
        )

    add_balance_to_accounts.short_description = "Adicionar saldo às contas das turmas selecionadas"



admin.site.register(Group, GroupAdmin)
