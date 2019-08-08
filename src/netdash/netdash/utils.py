from .netdash_modules import NetdashModule


def create_netdash_modules(modules):
    return [NetdashModule(module_name) for module_name in modules]
