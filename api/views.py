from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView

from service_monitor import ServiceMonitor


# TODO: soltanoff: use authentication.TokenAuthentication


class ApiRoot(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        return Response({
            'Services': reverse('api:services', request=request, format=format),
            'Failed services': reverse('api:failed_services', request=request, format=format),
        })


class EnabledServices(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        return Response(ServiceMonitor().get_enabled_services())


class ActiveServices(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        return Response(ServiceMonitor().get_active_services())


class InactiveServices(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        return Response(ServiceMonitor().get_inactive_services())


class FailedServices(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        return Response(ServiceMonitor().get_failed_services())


class ServiceStatus(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, service_name, format=None):
        return Response(ServiceMonitor().get_service_status(service_name))


class StartService(APIView):
    permission_classes = (permissions.IsAdminUser,)

    def post(self, request, service_name, format=None):
        return Response(ServiceMonitor().restart_service(service_name))


class StopService(APIView):
    permission_classes = (permissions.IsAdminUser,)

    def post(self, request, service_name, format=None):
        return Response(ServiceMonitor().stop_service(service_name))
