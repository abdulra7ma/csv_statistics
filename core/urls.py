from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

# Define Swagger API Schema
schema_view = get_schema_view(
    openapi.Info(
        title="ISAY FLY API",
        default_version="v1",
        description="",
        terms_of_service="",
        contact=openapi.Contact(email=""),
        license=openapi.License(name="Test License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

swagger_urlpatterns = [
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema_json",
    ),
    re_path(
        r"^swagger/$",
        schema_view.with_ui(
            "swagger",
            cache_timeout=0,
        ),
        name="schema_swagger_ui",
    ),
    re_path(
        r"^redoc/$",
        schema_view.with_ui(
            "redoc",
            cache_timeout=0,
        ),
        name="schema_redoc",
    ),
]

# include all your api endpoints here
api_urlpatterns = [path("statistics/", include("apps.statistics.api.urls"))]


urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "admin/doc/",
        include("django.contrib.admindocs.urls"),
    ),
    path("api/v1/", include(api_urlpatterns)),
    path("__debug__/", include("debug_toolbar.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# activate swagger urls
urlpatterns += swagger_urlpatterns
