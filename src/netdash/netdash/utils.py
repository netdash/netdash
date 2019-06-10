import importlib


def get_module_slug(module_name):
    module = importlib.import_module(module_name)
    module_slug = getattr(module, 'SLUG', None)
    if module_slug:
        return module_slug
    module_slug = module_name.replace('netdash_', '')
    module_slug = module_slug.split('_')[0]
    return module_slug


def get_module_settings(module_name):
    module = importlib.import_module(module_name)
    return module.SETTINGS_FROM_ENV
