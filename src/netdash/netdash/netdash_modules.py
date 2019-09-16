from importlib import import_module
from dataclasses import dataclass
from typing import Optional, List
from types import ModuleType
import traceback

from django.conf.urls import url, include, re_path


@dataclass
class Diagnostic:
    level: str  # 3.8: Literal["info", "suggestion", "warning", "error"]
    code: str   # 3.8: Literal["FAILED_IMPORT_UI", "FAILED_IMPORT_API", "FAILED_IMPORT_ALL",
    #           #              "NO_APP_NAME_UI", "NO_APP_NAME_API", "NO_APP_NAME_ALL"]
    message: str
    exception: Optional[Exception]
    traceback: Optional[str]


class NetDashModuleError(Exception):
    def __init__(self, app_label: str, diagnostics: List[Diagnostic]):
        self.diagnostics = diagnostics
        self.message = str(diagnostics)


class NetDashModule:
    _app_label: str
    _ui: Optional[ModuleType]
    _api: Optional[ModuleType]
    _app_name: str
    _diagnostics: List[Diagnostic]

    def __init__(self, app_label: str):
        self._diagnostics = []
        self._app_label = app_label
        self._ui = self._get_submodule(f'{app_label}.urls', 'UI')
        self._api = self._get_submodule(f'{app_label}.api.urls', 'API')
        if not (self._ui or self._api):
            self.diagnostics.append(Diagnostic(
                'error', 'FAILED_IMPORT_ALL',
                (
                    'Failed to import UI and API submodules. '
                    'At least one of the two must be present in a NetDash module. '
                    'Check FAILED_IMPORT_API and FAILED_IMPORT_UI diagnostics for more information.'
                ), None, None
            ))
            raise NetDashModuleError(app_label, self.diagnostics)
        derived_app_name = self._derive_app_name(self._ui, 'UI') or self._derive_app_name(self._api, 'API')
        if not derived_app_name:
            self.diagnostics.append(Diagnostic(
                'warning', 'NO_APP_NAME_ALL',
                (
                    f'No app_name was specified in {self.ui.__spec__.name} or {self.api.__spec__.name}. '
                    f'It will default to the app_label, {self._app_label}. '
                    f'Check NO_APP_NAME_UI and NO_APP_NAME_API diagnostics for more information.'
                ), None, None
            ))
        self._app_name = derived_app_name or self._app_label

    @property
    def diagnostics(self) -> List[Diagnostic]:
        return self._diagnostics

    @property
    def name(self) -> str:
        return self._app_label

    @property
    def friendly_name(self) -> str:
        return self._app_label.replace('_', ' ').title()

    @property
    def slug(self) -> str:
        return self._app_name

    @property
    def api_url(self) -> Optional[url]:
        return None if not self._api else self._generate_url('.api.urls')

    @property
    def ui_url(self) -> Optional[url]:
        return None if not self._ui else self._generate_url('.urls')

    def _generate_url(self, subpath: str) -> url:
        namespace_suffix = '-api' if 'api' in subpath else ''
        return re_path(r'^' + self.slug + '/', include(self._app_label + subpath, namespace=self.slug + namespace_suffix))

    def _derive_app_name(self, submodule: ModuleType, submodule_name: str) -> Optional[str]:
        try:
            raw = submodule.app_name
        except AttributeError as e:
            self._diagnostics.append(Diagnostic(
                'suggestion', f'NO_APP_NAME_{submodule_name}',
                (
                    f'app_name should be provided in {submodule_name}.'
                    f"It will provide the slugs for your module's routes."
                ), e, traceback.format_exc()
            ))
            return None
        return raw.replace('-api', '')

    def _get_submodule(self, module_path: str, submodule_name: str) -> Optional[ModuleType]:
        try:
            return import_module(module_path)
        except ModuleNotFoundError as ex:
            self._diagnostics.append(Diagnostic(
                'info', f'FAILED_IMPORT_{submodule_name}',
                (
                    f'Failed to import submodule {submodule_name} at {module_path}. '
                    f'If this module was intended to include a {submodule_name} within NetDash, '
                    f'please examine the stack trace to diagnose the error.'
                ), ex, traceback.format_exc()
            ))
            return None
