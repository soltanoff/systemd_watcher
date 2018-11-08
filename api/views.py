from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView

from service_monitor import ServiceMonitor


class ApiRoot(APIView):
    def get(self, request, format=None):
        return Response({
            'Active services': reverse('api:active_services', request=request, format=format),
            'Failed services': reverse('api:failed_services', request=request, format=format),
        })


class ListServices(APIView):
    permission_classes = (permissions.IsAdminUser,)

    def get(self, request, format=None):
        return Response(ServiceMonitor.get_service_list())


class FailedServices(APIView):
    permission_classes = (permissions.IsAdminUser,)

    def get(self, request, format=None):
        return Response(ServiceMonitor.get_failed_services())
