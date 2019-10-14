from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView

from service_monitor import ServiceMonitor
from watcher.models import FavoriteServiceModel


# TODO: soltanoff: use authentication.TokenAuthentication

favorite_services = FavoriteServiceModel.objects.values_list('name', flat=True).filter


class ApiRoot(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        return Response({
            'Services': reverse('api:services', request=request, format=format),
            'Failed services': reverse('api:failed_services', request=request, format=format),
            'Inactive services': reverse('api:inactive_services', request=request, format=format),
            'Favorite services': reverse('api:favorite_services', request=request, format=format),
        })


class StartService(APIView):
    permission_classes = (permissions.IsAdminUser,)

    def post(self, request, service_name, format=None):
        return Response(ServiceMonitor().restart_service(service_name))


class StopService(APIView):
    permission_classes = (permissions.IsAdminUser,)

    def post(self, request, service_name, format=None):
        return Response(ServiceMonitor().stop_service(service_name))


class ServiceStatus(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, service_name, format=None):
        return Response(ServiceMonitor().get_service_status(service_name))


class EnabledServices(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        return Response({
            'services': ServiceMonitor().get_enabled_services(),
            'favorite_services': favorite_services(user=request.user)
        })


class ActiveServices(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        return Response({
            'services': ServiceMonitor().get_active_services(),
            'favorite_services': favorite_services(user=request.user)
        })


class InactiveServices(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        return Response({
            'services': ServiceMonitor().get_inactive_services(),
            'favorite_services': favorite_services(user=request.user)
        })


class FailedServices(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        return Response(ServiceMonitor().get_failed_services())


class FavoriteServices(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        result = []
        monitor = ServiceMonitor()
        for service_name in favorite_services(user=request.user):
            service_status = monitor.get_service_status(service_name)
            if service_status:
                result.append(service_status)

        return Response(result)


class ManageFavoriteServices(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, service_name, format=None):
        record = FavoriteServiceModel.objects.filter(user=request.user, name=service_name).first()
        if record:
            record.delete()
        else:
            record = FavoriteServiceModel(user=request.user, name=service_name)
            record.save()

        return Response(favorite_services(user=request.user))
