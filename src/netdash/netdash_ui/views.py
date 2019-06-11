from django.http import HttpResponse
from django.template import loader
from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = 'netdash_ui/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['modules'] = []
        return context
