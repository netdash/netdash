from django.contrib.auth.models import AbstractUser, Group


class User(AbstractUser):
    def process_groups_saml(self, groups):
        existing_groups = list(filter(None, [Group.objects.filter(name=g).first() for g in groups]))
        self.groups.add(*existing_groups)
