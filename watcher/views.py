import operator

from django.views.generic import TemplateView

from service_monitor import ServiceMonitor


class ServiceView(TemplateView):
    template_name = "watcher/index.html"

    def get_context_data(self, **kwargs):
        kwargs['services'] = sorted(ServiceMonitor.iter_service_list(), key=operator.itemgetter('name'))
        return super(ServiceView, self).get_context_data(**kwargs)
