from django.contrib.auth.models import AbstractUser, Group
from django.dispatch import receiver
from django.db.models.signals import post_save

DEFAULT_GROUP = 'Default'


class User(AbstractUser):
    def process_groups(self, group_names):
        self._ensure_groups_created_and_added(group_names)
        self._remove_revoked_group_memberships(group_names)

    def _ensure_groups_created_and_added(self, group_names):
        groups = [Group.objects.get_or_create(name=g)[0] for g in group_names]
        self.groups.add(*groups)

    def _remove_revoked_group_memberships(self, group_names):
        revoked_groups = self.groups.exclude(name__in=group_names)
        self.groups.remove(*revoked_groups)


@receiver(post_save, sender=User)
def post_save_user_signal_handler(sender, instance, created, **kwargs):
    if created:
        group, group_created = Group.objects.get_or_create(name=DEFAULT_GROUP)
        instance.groups.add(group)
        instance.save()
