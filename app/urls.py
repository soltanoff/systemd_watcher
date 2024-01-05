from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from rest_framework.authtoken import views
from rest_framework.schemas import get_schema_view

urlpatterns = [
    path('', include('watcher.urls')),
    path('accounts/', include('account.urls')),
    path('manage/', admin.site.urls),
    path('schema/', get_schema_view(title='Test API')),
    path('api/v1/', include('api.urls')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api-token-auth/', views.obtain_auth_token)
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
