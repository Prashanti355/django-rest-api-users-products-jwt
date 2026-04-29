from django.contrib import admin
from django.urls import include, path

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

from apps.users.auth_views import (
    CustomTokenObtainPairView,
    CustomTokenRefreshView,
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include("apps.users.urls")),
    path("api/v1/", include("apps.products.urls")),
    path("api/v1/", include("apps.audit.urls")),
    path(
        "api/v1/auth/login/",
        CustomTokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path(
        "api/v1/auth/refresh/", CustomTokenRefreshView.as_view(), name="token_refresh"
    ),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]
