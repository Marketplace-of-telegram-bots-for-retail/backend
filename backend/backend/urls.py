from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('api/', include('api.urls')),
    path('admin/', admin.site.urls),
    path(
        'docs/',
        SpectacularSwaggerView.as_view(
            url_name='schema',
        ),
        name='swagger-ui',
    ),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
    urlpatterns += [
        path('__debug__/', include('debug_toolbar.urls')),
    ]
