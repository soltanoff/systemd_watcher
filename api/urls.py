from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from api import views
from api.apps import ApiConfig

app_name = ApiConfig.name
urlpatterns = format_suffix_patterns([
    url(r'^$', views.ApiRoot.as_view()),
    url(r'^services/$', views.ListServices.as_view(), name='services'),
    url(r'^services/failed/$', views.FailedServices.as_view(), name='failed_services'),
    url(r'^service/status/<service_name>/$', views.ServiceStatus.as_view(), name='service_status'),
    url(r'^service/start/<service_name>/$', views.StartService.as_view(), name='start_services'),
    url(r'^service/restart/<service_name>/$', views.StartService.as_view(), name='restart_services'),
    url(r'^service/stop/<service_name>/$', views.StopService.as_view(), name='stop_services'),
])
