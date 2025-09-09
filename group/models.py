from django.db import models
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from account.models import Account, AccountType


class Group(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="nome")
    icon = models.FileField(upload_to="icons/", verbose_name="ícone")
    begin = models.DateField(verbose_name="data de ínicio")
    end = models.DateField(verbose_name="data de fim")
    accounts = models.ManyToManyField(
        Account, related_name="group", blank=True, verbose_name="contas"
    )

    def __str__(
        self,
    ):
        return f"#{self.id} | {self.name}"


@receiver(m2m_changed, sender=Group.accounts.through)
def update_account_on_group_change(
    sender, instance, action, reverse, model, pk_set, **kwargs
):
    if action == "post_add":
        for account_id in pk_set:
            account = model.objects.get(pk=account_id)
            if not account.type == AccountType.ADMIN.value:
                account.type = AccountType.PREMIUM.value
                account.save()

    elif action == "post_remove":
        for account_id in pk_set:
            account = model.objects.get(pk=account_id)
            if not account.group.all() and not account.type == AccountType.ADMIN.value:
                account.type = AccountType.FREE.value
            account.save()
