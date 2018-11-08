from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView

from service_monitor import ServiceMonitor


class ApiRoot(APIView):
    def get(self, request, format=None):
        return Response({
            'services': reverse('api:services', request=request, format=format),
        })


class ListServices(APIView):
    permission_classes = (permissions.IsAdminUser,)

    def get(self, request, format=None):
        return Response(ServiceMonitor.get_service_list())
