from django.contrib import admin
from django.http import JsonResponse
from django.urls import include, path
from django.views.decorators.http import require_GET

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

from apps.users.auth_views import (
    CustomTokenObtainPairView,
    CustomTokenRefreshView,
)