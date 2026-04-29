from django.contrib import admin
from django.urls import include, path
from drf_spectacular.utils import extend_schema
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

TokenObtainPairView = extend_schema(
    tags=["Authentication"],
)(TokenObtainPairView)

TokenRefreshView = extend_schema(
    tags=["Authentication"],
)(TokenRefreshView)


urlpatterns = [
    path("admin/", admin.site.urls),

    path("api/v1/", include("apps.users.urls")),
    path("api/v1/", include("apps.products.urls")),

    path("api/v1/auth/login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/v1/auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]