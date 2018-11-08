from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from api.apps import ApiConfig
from api.views import ListServices, ApiRoot

app_name = ApiConfig.name
urlpatterns = format_suffix_patterns([
    path('', ApiRoot.as_view()),
    path('services/', ListServices.as_view(), name='services'),
])
