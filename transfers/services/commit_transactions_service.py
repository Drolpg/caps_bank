from django.conf import settings
from django.template.loader import render_to_string

from caps_bank.tasks import celery_send_mail


class CommitTrasactionService:
    def __init__(self, transaction):
        self.from_account = transaction.from_account
        self.to_account = transaction.to_account
        self.amount = transaction.amount
        self.transaction = transaction

    def success_send_mail(self):
        subject_sender = "Transação Confirmada"
        html_content_sender = render_to_string(
            "email/transaction_confirmed.html",
            {
                "from_account": self.from_account,
                "to_account": self.to_account,
                "amount": self.amount,
            },
        )
        email_to_sender = self.from_account.email

        subject_receiver = "Você recebeu uma transação"
        html_content_receiver = render_to_string(
            "email/transaction_received.html",
            {
                "from_account": self.from_account,
                "to_account": self.to_account,
                "amount": self.amount,
            },
        )
        email_to_receiver = self.to_account.email

        if settings.USING_REDIS:
            celery_send_mail.delay(
                subject_sender,
                html_content_sender,
                settings.DEFAULT_FROM_EMAIL,
                email_to_sender,
            )

            celery_send_mail.delay(
                subject_receiver,
                html_content_receiver,
                settings.DEFAULT_FROM_EMAIL,
                email_to_receiver,
            )
        else:
            celery_send_mail(
                subject_sender,
                html_content_sender,
                settings.DEFAULT_FROM_EMAIL,
                email_to_sender,
            )

            celery_send_mail(
                subject_receiver,
                html_content_receiver,
                settings.DEFAULT_FROM_EMAIL,
                email_to_receiver,
            )

    def canceled_transaction_send_mail(self):
        subject = "Transação Cancelada"
        html_content = render_to_string(
            "email/transaction_canceled.html",
            {
                "from_account": self.from_account,
                "to_account": self.to_account,
                "amount": self.amount,
            },
        )
        email_from = settings.DEFAULT_FROM_EMAIL
        email_to = self.from_account.email

        if settings.USING_REDIS:
            celery_send_mail.delay(subject, html_content, email_from, email_to)
        else:
            celery_send_mail(subject, html_content, email_from, email_to)

    def make_transaction(self):
        if self.from_account.balance < self.amount:
            self.canceled_transaction_send_mail()
            self.transaction.delete()
            return

        self.from_account.balance -= self.amount
        self.to_account.balance += self.amount
        self.transaction.is_committed = True

        self.from_account.save()
        self.to_account.save()
        self.transaction.save()
        self.success_send_mail()
