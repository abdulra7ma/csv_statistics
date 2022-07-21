# Django imports
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

# app imports
from .swagger.urls import swagger_urlpatterns

# include all your api endpoints here
api_urlpatterns = [path("statistics/", include("apps.statistics.api.urls"))]


urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "admin/doc/",
        include("django.contrib.admindocs.urls"),
    ),
    path("api/v1/", include(api_urlpatterns)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# activate swagger urls
urlpatterns += swagger_urlpatterns
