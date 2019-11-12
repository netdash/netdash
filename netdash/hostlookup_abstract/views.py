from typing import Iterable, Optional
from abc import ABC, abstractmethod

from django.views.generic.base import TemplateView
from django.core.exceptions import ValidationError

from .utils import HostLookupResult


class BaseHostLookupView(ABC, TemplateView):
    template_name = "hostlookup/hostlookupresult_list.html"

    @abstractmethod
    def host_lookup(self, **kwargs) -> Optional[Iterable[HostLookupResult]]:
        return NotImplemented

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            results = self.host_lookup(**kwargs)
        except ValidationError as ve:
            context['errors'] = ve
            return context
        context['results'] = results
        return context
