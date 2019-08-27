from .netdash_modules import NetDashModule


def create_netdash_modules(modules):
    return [NetDashModule(module_name) for module_name in modules]
