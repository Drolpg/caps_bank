from django.utils import timezone
from transfers.models import Transaction
from django.template.loader import render_to_string
from django.conf import settings
import random, string, os
from caps_bank.tasks import celery_send_mail, celery_send_mail


class TransactionTokenService:
    def __init__(self, transaction_data):
        self.transaction_data = transaction_data
        self.token = None
        self.token_expiration = None

    def generate_token(self):
        self.token = ''.join(random.choices(string.digits, k=6))  
        expiration_minutes = int(os.getenv('TOKEN_EXPIRATION_MINUTES', 5))
        self.token_expiration = timezone.now() + timezone.timedelta(minutes=expiration_minutes)
        self.send_token_email() 

    def send_token_email(self):
        subject = "Token para confirmação da transferência"

        html_content = render_to_string("email/token_confirmation.html", {
            "from_account": self.transaction_data['from_account'],
            "token": self.token,
            "token_expiration": self.token_expiration.strftime("%H:%M:%S")
        })

        email_from = settings.DEFAULT_FROM_EMAIL
        email_to = self.transaction_data['from_account'].email

        if settings.USING_REDIS:
            celery_send_mail.delay(
                subject, html_content, email_from, email_to
            )
        else:
            celery_send_mail(
                subject, html_content, email_from, email_to
            )

    def confirm_transaction(self, token_input):
        if self.token_expiration <= timezone.now():
            return "O token expirou. Por favor, solicite um novo token."

        if self.token == token_input:
            transaction = Transaction(
                from_account=self.transaction_data["from_account"],
                to_account=self.transaction_data["to_account"],
                amount=self.transaction_data["amount"],
                token=self.token,
            )
            transaction.save()
            return "Transação confirmada com sucesso!"
        
        return "Token inválido. Por favor, verifique e tente novamente."
