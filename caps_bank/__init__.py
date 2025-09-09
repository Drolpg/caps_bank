from __future__ import absolute_import, unicode_literals
from .celery import app as celery_app
import os


def load_env_file(filepath=".env"):
    if os.path.exists(filepath):
        with open(filepath) as f:
            for line in f:
                if line.strip() and not line.startswith("#"):
                    key, value = line.strip().split("=", 1)
                    os.environ[key] = value


load_env_file()
__all__ = ("celery_app",)
