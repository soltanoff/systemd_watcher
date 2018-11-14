from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from api import views
from api.apps import ApiConfig

app_name = ApiConfig.name
urlpatterns = format_suffix_patterns([
    path('', views.ApiRoot.as_view()),
    path('services/', views.ListServices.as_view(), name='services'),
    path('services/failed/', views.FailedServices.as_view(), name='failed_services'),
    path('service/status/<service_name>/', views.ServiceStatus.as_view(), name='service_status'),
    path('service/start/<service_name>/', views.StartService.as_view(), name='start_services'),
    path('service/restart/<service_name>/', views.StartService.as_view(), name='restart_services'),
    path('service/stop/<service_name>/', views.StopService.as_view(), name='stop_services'),
])