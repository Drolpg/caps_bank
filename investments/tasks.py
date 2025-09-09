from investments.utils import get_selic_rate, get_cdi_rate, get_tjlp_rate
from .models import Indexer, Investment
from celery import shared_task
from django.utils import timezone


@shared_task(bind=True, max_retries=5, default_retry_delay=60)
def update_income(self):
    investments = Investment.objects.filter(status="ativo")
    try:
        for investment in investments:
            investment.update_income()
            investment.save()
            print(
                f"Investimento de {investment.account} atualizado com sucesso!"
                )
    except Exception as exc:
        raise self.retry(exc=exc)
    return "Atualização concluída com sucesso!"


@shared_task(bind=True, max_retries=5, default_retry_delay=60)
def update_selic(self):
    selic_indexer, _ = Indexer.objects.get_or_create(
        name="SELIC")
    try:
        selic_rate = get_selic_rate()
        if not selic_rate:
            raise Exception("Não foi possível obter a taxa SELIC")
        selic_indexer.rate = selic_rate
        selic_indexer.save()
    except Exception as exc:
        raise self.retry(exc=exc)
    return f"Indexador SELIC atualizado: {selic_indexer.rate}"


@shared_task(bind=True, max_retries=5, default_retry_delay=60)
def update_cdi(self):
    cdi_indexer, _ = Indexer.objects.get_or_create(name="CDI")
    try:
        cdi_rate = get_cdi_rate()
        if not cdi_rate:
            raise Exception("Não foi possível obter a taxa CDI")
        cdi_indexer.rate = cdi_rate
        cdi_indexer.save()
    except Exception as exc:
        raise self.retry(exc=exc)
    return f"Indexador CDI atualizado: {cdi_indexer.rate}"


@shared_task(bind=True, max_retries=5, default_retry_delay=60)
def update_tjlp(self):
    tjlp_indexer, _ = Indexer.objects.get_or_create(name="TJLP")
    try:
        tjlp_rate = get_tjlp_rate()
        if not tjlp_rate:
            raise Exception("Não foi possível obter a taxa TJLP")
        tjlp_indexer.rate = tjlp_rate
        tjlp_indexer.save()
    except Exception as exc:
        raise self.retry(exc=exc)
    return f"Indexador TJLP atualizado: {tjlp_indexer.rate}"


@shared_task(bind=True, max_retries=5, default_retry_delay=60)
def finalize_investments(self):
    expired_investments = Investment.objects.filter(
        rescue_date__lt=timezone.now(),
        status="ativo"
        )
    try:
        for investment in expired_investments:
            investment.rescue_investment("vencido")
            print(
                f"""Investimento de {
                    investment.account
                    } vencido, valor resgatado: {
                        (
                            investment.accumulated_income +
                            investment.applied_value
                        )
                        }!"""
            )
    except Exception as exc:
        raise self.retry(exc=exc)
    return "Investimentos expirados resgatados"
