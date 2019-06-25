import importlib
import logging

from django.conf import settings

logger = logging.getLogger(__name__)


def flatten(l): return [item for sublist in l for item in sublist]


def get_module_slug(module_name):
    try:
        module = importlib.import_module(f'{module_name}.urls')
    except ModuleNotFoundError as e1:
        logger.warning(f'Failed to import urls.py for module: {module_name}')
        logger.info(e1, exc_info=True)
        try:
            module = importlib.import_module(f'{module_name}.api.urls')
        except ModuleNotFoundError as e2:
            raise Exception(f'Failed to import both urls.py and api/urls.py for module: {module_name}') from e2
    if hasattr(module, 'app_name'):
        if module.app_name.endswith('-api'):
            return module.app_name.replace('-api', '')
        return module.app_name
    return module_name.replace('netdash_', '').split('_')[0]


def get_module_slugs():
    return {m: get_module_slug(m) for m in settings.NETDASH_MODULES}


def get_module_settings(module_name):
    module = importlib.import_module(module_name)
    return getattr(module, 'SETTINGS_FROM_ENV', [])
