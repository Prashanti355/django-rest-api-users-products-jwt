from apps.users.auth_views import (
    CustomTokenObtainPairView,
    CustomTokenRefreshView,
)
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from django.http import JsonResponse
from django.views.decorators.http import require_GET
@require_GET
def health_check(request):
    return JsonResponse(
        {
            "status": "ok",
            "service": "django-rest-api-users-products-jwt",
        }
    )

urlpatterns = [
    path("", health_check, name="root-health-check"),
    path("api/health/", health_check, name="health-check"),

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
