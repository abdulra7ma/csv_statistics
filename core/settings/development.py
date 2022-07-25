from .common import *
from .environment import env

# ##### DEBUG CONFIGURATION ###############################
DEBUG = env.bool("DEBUG", default=False)

# allow all hosts during development
ALLOWED_HOSTS = ["*"]

DATABASES = {
    "default": env.db("CORE_DATABASE_URL", default="psql://postgres:statistics_password_1@127.0.0.1:5432/statistics_db")
}

# ##### APPLICATION CONFIGURATION #########################

INSTALLED_APPS = DEFAULT_APPS


if DEBUG:
    import socket  # only if you haven't already imported this

    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS = [ip[: ip.rfind(".")] + ".1" for ip in ips] + ["127.0.0.1", "10.0.2.2"]


REST_FRAMEWORK = {
    "EXCEPTION_HANDLER": "rest_framework.views.exception_handler",
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 100,
    "DEFAULT_FILTER_BACKENDS": ("django_filters.rest_framework.DjangoFilterBackend",),
}


# Swagger Settings
SWAGGER_SETTINGS = {
    "SECURITY_DEFINITIONS": {
        "Auth Token eg [Bearer (JWT)]": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "flow": "Bearer",
        },
    },
}