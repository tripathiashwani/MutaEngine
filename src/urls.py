from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

api_prefix: str = "api"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("ckeditor5/", include('django_ckeditor_5.urls')),
    path(
        "schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
    path(
        f"{api_prefix}/",
        include(
            [
                path(
                    "v1/",
                    include(
                        [
                            path("mail/", include("src.apps.mail.urls")),
                            path("company/", include("src.apps.company.urls")),
                            path("job/", include("src.apps.job.urls")),
                            path("applicant/",include("src.apps.applicant.urls")),
                            path("auth/", include("src.apps.auth.urls")),
                        ]
                    ),
                )
            ]
        ),
    ),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
