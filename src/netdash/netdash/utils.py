import importlib


def get_module_slug(module_name):
    module = importlib.import_module(module_name)
    if hasattr(module, 'SLUG'):
        return module.SLUG
    return module_name.replace('netdash_', '').split('_')[0]


def get_module_settings(module_name):
    module = importlib.import_module(module_name)
    return getattr(module, 'SETTINGS_FROM_ENV', [])
