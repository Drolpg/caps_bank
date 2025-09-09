from celery import shared_task
from .models import Transaction
from .services.commit_transactions_service import CommitTrasactionService

@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def commit_transactions(self):
    transactions_uncommitted = Transaction.objects.filter(is_committed=False)
    for transaction in transactions_uncommitted:
        commit_service = CommitTrasactionService(transaction)
        commit_service.make_transaction()
