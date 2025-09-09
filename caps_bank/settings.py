"""
Django settings for caps_bank project.

Gerado por 'django-admin startproject' usando Django 4.2.12.
"""

from pathlib import Path
from celery.schedules import crontab
import os

# ==========================
# Caminhos base
# ==========================
BASE_DIR = Path(__file__).resolve().parent.parent

# ==========================
# Segurança
# ==========================
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "unsafe-secret-key")
DEBUG = os.getenv("DEBUG", "False") == "True"
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "*").split(",")

AUTH_USER_MODEL = "account.Account"

# ==========================
# Apps
# ==========================
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "account",
    "group",
    "investments",
    "transfers",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "caps_bank.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "caps_bank.wsgi.application"

# ==========================
# Banco de Dados
# ==========================
DATABASES = {
    "default": {
        "ENGINE": os.getenv("DATABASE_ENGINE", "django.db.backends.postgresql"),
        "NAME": os.getenv("POSTGRES_DB", "capsbank"),
        "USER": os.getenv("POSTGRES_USER", "postgres"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD", "postgres"),
        "HOST": os.getenv("POSTGRES_HOST", "db"),
        "PORT": os.getenv("POSTGRES_PORT", "5432"),
    }
}

# ==========================
# Validação de senha
# ==========================
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ==========================
# Internacionalização
# ==========================
LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Sao_Paulo"
USE_TZ = False
SITE_ID = 1

# ==========================
# Arquivos estáticos e mídia
# ==========================
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# ==========================
# Email
# ==========================
EMAIL_BACKEND = os.getenv(
    "EMAIL_BACKEND", "django.core.mail.backends.smtp.EmailBackend"
)
EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", 587))
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", "True") == "True"
EMAIL_USE_SSL = os.getenv("EMAIL_USE_SSL", "False") == "True"
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", EMAIL_HOST_USER)

# ==========================
# Celery
# ==========================
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0")
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "redis://redis:6379/0")
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = (
    os.getenv("CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP", "True") == "True"
)
USING_REDIS = os.getenv("USING_REDIS", "True") == "True"

CELERY_BEAT_SCHEDULE = {
    "update-income-every-morning": {
        "task": "investments.tasks.update_income",
        "schedule": crontab(hour=8, minute=0),
    },
    "update-selic-indexer-every-morning": {
        "task": "investments.tasks.update_selic",
        "schedule": crontab(hour=8, minute=0),
    },
    "update-cdi-indexer-every-morning": {
        "task": "investments.tasks.update_cdi",
        "schedule": crontab(hour=8, minute=0),
    },
    "update-tjlp-indexer-every-morning": {
        "task": "investments.tasks.update_tjlp",
        "schedule": crontab(hour=8, minute=0),
    },
    "finalize-expired-investments-every-day": {
        "task": "investments.tasks.finalize_investments",
        "schedule": crontab(hour=0, minute=1),
    },
    "process_uncommitted_transactions_every_weekday_at_8am": {
        "task": "transfers.tasks.commit_transactions",
        "schedule": crontab(hour=8, minute=0, day_of_week="1-5"),
    },
}

# ==========================
# Autenticação
# ==========================
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",  # Backend padrão
]

LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

# ==========================
# Configuração padrão de PK
# ==========================
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
