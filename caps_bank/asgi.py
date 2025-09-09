"""
ASGI config for caps_bank project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

from investments.tasks import update_selic, update_tjlp, update_cdi

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'caps_bank.settings')

update_selic.delay()
update_tjlp.delay()
update_cdi.delay()

application = get_asgi_application()
