from typing import Iterable
from abc import ABC, abstractmethod

from django.views.generic.base import TemplateView

from .utils import HostLookupResult


class BaseHostLookupView(ABC, TemplateView):
    template_name = "hostlookup/hostlookupresult_list.html"

    @abstractmethod
    def host_lookup(self, **kwargs) -> Iterable[HostLookupResult]:
        return NotImplemented

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        results = self.host_lookup(**kwargs)
        context['results'] = results
        return context
