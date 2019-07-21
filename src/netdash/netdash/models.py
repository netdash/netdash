from django.contrib.auth.models import AbstractUser, Group


class User(AbstractUser):
    def process_groups(self, group_names):
        self._ensure_groups_created_and_added(group_names)
        self._remove_revoked_group_memberships(group_names)

    def _ensure_groups_created_and_added(self, group_names):
        groups = [Group.objects.get_or_create(name=g) for g in group_names]
        self.groups.add(groups)

    def _remove_revoked_group_memberships(self, group_names):
        revoked_groups = self.groups.exclude(name__in=group_names)
        self.groups.remove(*revoked_groups)
