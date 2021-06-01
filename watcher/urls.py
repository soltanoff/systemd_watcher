from django.contrib.auth.decorators import login_required
from django.urls import path

from watcher import views
from watcher.apps import WatcherConfig

app_name = WatcherConfig.name
urlpatterns = [
    path(r'', login_required(views.ServiceView.as_view()), name='index'),
]
