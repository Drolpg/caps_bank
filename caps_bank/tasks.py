from celery import shared_task
from django.core.mail import EmailMultiAlternatives


@shared_task(bind=True, max_retries=3, default_retry_delay=60)  
def celery_send_mail(self,subject, html_content, from_email, to_email):
    email = EmailMultiAlternatives(subject, html_content, from_email, [to_email])
    email.attach_alternative(html_content, "text/html")
    email.send()
