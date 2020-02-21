# Module Conventions

* A module with `urls.py` should declare an `app_name`.
* A module with `urls.py` will have its URLs placed under `/<app_name>/*`.
* A module with `urls.py` should have a url named `index`. A link to `index` will be generated in the NetDash navbar.
* A module that generates a permission named `can_view_module` will only generate an `index` link in the NetDash navbar for users who have that permission.
* A module with `api/urls.py` should declare an `app_name`. If the module also has a `urls.py`, it should reuse the previous `app_name` like so: `<app_name>-api`
* A module with `api/urls.py` will have its API URLs placed under `/api/<app_name>/*`.
* Modules should include a `README.md` in their root that describes settings, package dependencies, and required integrations.
* Required permissions of module views should be set in `urls.py` rather than `views.py`. This allows for the extension of views without inheriting their required permissions.

Check the [example apps](https://github.com/netdash/netdash-examples) for examples of these conventions.

## Default Group
Every user created is added to a group named: `Default`. This group gives NetDash the the capability to allow certain modules to be accessed by any user in the server.
* To make a NetDash module available to the default group, the module's `can_view_module` permission must be given to the `Default` group through the admin website.
