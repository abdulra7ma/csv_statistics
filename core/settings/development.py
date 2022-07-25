from datetime import datetime
from os.path import join

from .common import *
from .environment import env

# uncomment the following line to include i18n
# from .i18n import *

# ##### DEBUG CONFIGURATION ###############################
DEBUG = env.bool("DEBUG", default=False)

# allow all hosts during development
ALLOWED_HOSTS = ["*"]

# adjust the minimal login
# LOGIN_URL = "core_login"
# LOGIN_REDIRECT_URL = "/"
# LOGOUT_REDIRECT_URL = "core_login"


##### DATABASE CONFIGURATION ############################
# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": join(PROJECT_ROOT, "run", "dev.sqlite3"),
#     }
# }

DATABASES = {
    "default": env.db("CORE_DATABASE_URL", default="psql://postgres:statistics_password_1@127.0.0.1:5432/statistics_db")
}

# ##### APPLICATION CONFIGURATION #########################

INSTALLED_APPS = DEFAULT_APPS

# INTERNAL_IPS = [
#     "127.0.0.1",
# ]

if DEBUG:
    import socket  # only if you haven't already imported this

    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS = [ip[: ip.rfind(".")] + ".1" for ip in ips] + ["127.0.0.1", "10.0.2.2"]


# ##### CORS CONFIGURATION ############################
# CORS_ORIGIN_ALLOW_ALL = False
# CORS_ORIGIN_WHITELIST = ("http://localhost:3000",)


# #####  CELERY CONFIGURATION############################
# CELERY_BROKER_URL = "redis://localhost:6379"
# CELERY_RESULT_BACKEND = "redis://localhost:6379"
# CELERY_ACCEPT_CONTENT = ["application/json", "pickle"]
# CELERY_TASK_SERIALIZER = "json"
# CELERY_RESULT_SERIALIZER = "json"
# CELERY_TIMEZONE = "Asia/Bishkek"
# CELERY_IMPORTS = ("apps.app.workers.tasks",)


# #####  DJANGO LOGGING CONFIGURATION############################
# LOGGING = {
#     "version": 1,
#     "filters": {
#         "require_debug_true": {
#             "()": "django.utils.log.RequireDebugTrue",
#         }
#     },
#     "handlers": {
#         "console": {
#             "level": "DEBUG",
#             "filters": ["require_debug_true"],
#             "class": "logging.StreamHandler",
#         },
#         "file": {
#             "level": "DEBUG",
#             "class": "logging.FileHandler",
#             "filename": f"{PROJECT_ROOT}/logs/django/debug.log",
#         },
#     },
#     "loggers": {
#         "django.db.backends": {
#             "level": "DEBUG",
#             "handlers": ["console"],
#             'formatter': 'verbose'
#         }
#     },
#     "formatters": {
#         "verbose": {
#             "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
#             "style": "{",
#         },
#         "simple": {
#             "format": "{levelname} {message}",
#             "style": "{",
#         },
#     },
# }
