from django.urls import path

from account import views
from account.apps import AccountConfig

app_name = AccountConfig.name
urlpatterns = [
    path(r'login/', views.CustomLoginView.as_view(), name='login'),
    path(r'logout/', views.logout, name='logout'),
]
