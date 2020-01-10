'''
Create a Public Group where each user gets viewing access to all modules
'''
import logging

from django.conf import settings
from django.contrib.auth.models import Group, Permission
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Creates a Public group and gives viewing permissions to all users'

    def handle(self, *args, **options):
        GROUPNAME = "Public"
        PERMISSION_CODENAME = "can_view_module"

        new_group, created = Group.objects.get_or_create(name=GROUPNAME)
        from django.apps import apps
        print(apps.get_app_configs())
        for module in settings.NETDASH_MODULES:
            try:
                viewing_permission = Permission.objects.get(content_type__app_label=module,
                                                            codename=f"{PERMISSION_CODENAME}")
            except Permission.DoesNotExist:
                logging.warning(f"Permission not found with name '{PERMISSION_CODENAME}' in {module}")
            else:
                new_group.permissions.add(viewing_permission)

        logging.info("Created Public group with viewing permissions")

        User = get_user_model()

        users = User.objects.all()

        for user in users:
            new_group.user_set.add(user)
