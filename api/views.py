from rest_framework import permissions, authentication
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView

from service_monitor import ServiceMonitor


class ApiRoot(APIView):
    def get(self, request, format=None):
        return Response({
            'Services': reverse('api:services', request=request, format=format),
            'Failed services': reverse('api:failed_services', request=request, format=format),
        })


class ListServices(APIView):
    def get(self, request, format=None):
        return Response(ServiceMonitor.get_service_list())


class FailedServices(APIView):
    def get(self, request, format=None):
        return Response(ServiceMonitor.get_failed_services())


class ServiceStatus(APIView):
    def get(self, request, service_name, format=None):
        return Response(ServiceMonitor.get_service_status(service_name))


class StartService(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser,)

    def post(self, request, service_name, format=None):
        return Response(ServiceMonitor.set_restart_service(service_name))


class StopService(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser,)

    def post(self, request, service_name, format=None):
        return Response(ServiceMonitor.set_stop_service(service_name))
