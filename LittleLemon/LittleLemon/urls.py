"""
--------------------------------------------------------------------------
Little Lemon Project - Main URL Configuration
--------------------------------------------------------------------------

This file defines the root URL routes for the Django project.

Included Routes:
- /admin/        -> Django admin panel
- /auth/         -> Djoser authentication endpoints (token-based login, logout, registration, etc.)
- /api/          -> Application API endpoints (menu items, cart, orders, user management, etc.)

Note:
- Djoser is used for user authentication and token management.
- App-specific URLs are included from 'LittleLemonAPI.urls'.

For more details on Django URL routing:
https://docs.djangoproject.com/en/5.2/topics/http/urls/

--------------------------------------------------------------------------
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('api/', include('LittleLemonAPI.urls')),
]
