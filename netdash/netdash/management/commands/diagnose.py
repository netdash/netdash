from django.core.management.base import BaseCommand
from django.conf import settings

from netdash import utils


class Command(BaseCommand):
    help = 'Check the diagnostics of all listed NetDash modules. Set verbosity > 1 to include tracebacks.'

    _styles = {
        'info': 'SUCCESS',
        'suggestion': 'NOTICE',
        'warning': 'WARNING',
        'error': 'ERROR',
    }

    def handle(self, *test_labels, **options):
        modules = utils.create_netdash_modules(settings.NETDASH_MODULES)
        for m in modules:
            self.stdout.write(f'{m.name}\n{"-" * len(m.name)}')
            if not len(m.diagnostics):
                self.stdout.write(self.style.SUCCESS('No problems found.'))
            for d in m.diagnostics:
                self.stdout.write(getattr(self.style, self._styles[d.level])(d.message))
                if options['verbosity'] > 1:
                    self.stdout.write(getattr(self.style, self._styles[d.level])(d.traceback))
            self.stdout.write('\n')
