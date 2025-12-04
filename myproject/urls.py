from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

ADMIN_URL = getattr(settings, 'ADMIN_URL', 'admin/')

admin.site.site_header = "Админ-панель"

urlpatterns = [
    path(ADMIN_URL, admin.site.urls),
    path('', include('core.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
