from django.core.management.commands import test
from django.conf import settings


class Command(test.Command):
    help = 'Discover and run tests in NETDASH_MODULES'

    def run_from_argv(self, argv):
        super(Command, self).run_from_argv(argv)

    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)

    def handle(self, *test_labels, **options):
        import os
        import sys
        sys.stdout.write(os.getcwd())
        if not test_labels:
            test_labels = settings.NETDASH_MODULES
        super().handle(*test_labels, **options)
