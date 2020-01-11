# Enable Public Group

```bash
python manage.py enable_public_group [-h] [--nousers]
```

This command results in the creation of a group named "Public" with permissions to view all the modules in a NetDash instance that generate the permission named `can_view_module`. All existing users are added to this group by default. To prevent this, run the command with the `--nousers` flag.
