from django.contrib.auth.decorators import login_required
from django.urls import path

from watcher.apps import WatcherConfig
from watcher.views import ServiceView

app_name = WatcherConfig.name
urlpatterns = [
    path(r'', login_required(ServiceView.as_view()), name='index'),
]
