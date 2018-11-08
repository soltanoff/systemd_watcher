from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from api import views
from api.apps import ApiConfig

app_name = ApiConfig.name
urlpatterns = format_suffix_patterns([
    path('', views.ApiRoot.as_view()),
    path('active_services/', views.ListServices.as_view(), name='active_services'),
    path('failed_services/', views.FailedServices.as_view(), name='failed_services'),
])
