import importlib
import sys

class NetdashModule():
    
    def _get_app_name(self, app_label):
        diagnostics = []

        try:
            module = importlib.import_module(f'{app_label}.urls')
        except ModuleNotFoundError as e1:
            print(f'Failed to import urls.py for module: {app_label}')
            try:
                module = importlib.import_module(f'{app_label}.api.urls')
            except ModuleNotFoundError as e2:
                print(f'Failed to import both urls.py and api/urls.py for module: {app_label}')
            else:
                print('api module has been imported')

        return app_label, diagnostics

    def __init__(self, app_label):
        self.app_name, diagnostics = self._get_app_name(app_label)
