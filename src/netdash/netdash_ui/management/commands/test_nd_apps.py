from django.core.management.commands import test


class Command(test.Command):
    help = 'Discover and run tests in the specifiied modules or in the apps_dev directory'

    def run_from_argv(self, argv):
        super(Command, self).run_from_argv(argv)

    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)

    def handle(self, *test_labels, **options):
        import os
        import sys
        sys.stdout.write(os.getcwd())
        if not test_labels:
            test_labels = ["../../apps_dev/", ]
        super().handle(*test_labels, **options)
