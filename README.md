![NetDash](docs/netdash-logo-small.png)

The NetDash project's goal is to create an interface to allow delegation of specific IT infrastructure management tasks to IT teams outside of a central IT team. 

## Getting Started

1. Clone this repository.
2. Change to the new directory: `cd netdash`
3. Copy the example settings to use them: `cp netdash/netdash/settings_example.py netdash/netdash/settings.py`
4. Install dependencies: `pip install requirements.deploy.txt`
5. Run migrations: `python netdash/manage.py migrate`
6. Run the development server: `python netdash/manage.py runserver`

## Creating a NetDash Module

A *NetDash Module* is a Django App that follows certain conventions and thereby integrates automatically with NetDash without any additional code changes. These integrations include UI link generation, Swagger API inclusion, routing and permissions.

1. Change directory to NetDash apps: `cd netdash`
2. Create a new NetDash Module, substituting `my_custom_nd_module` for your module's name: `python manage.py startapp --template ../../netdash_module_template my_custom_nd_module`
3. Run its initial migration: `python manage.py migrate`
4. Exclude your app from NetDash's source control, substituting `my_custom_nd_module` for your module's name: `echo netdash/my_custom_nd_module >> ../../.git/info/exclude`
5. Navigate into your app's directory and initialize a new git repo: `cd my_custom_nd_module; git init`
6. To enable your new module, add your module's name to `NETDASH_MODULES` in `settings.py`:
    ```
    NETDASH_MODULES = [
        'my_custom_nd_module',
    ]
    ```
    NetDash Modules can be specified as Django app labels or as paths to an AppConfig [the same way that `settings.INSTALLED_APPS` is configured](https://docs.djangoproject.com/en/2.2/ref/applications/#for-application-users).
7. Restart the development server.
8. *(Optional)* If your NetDash Module requires additional packages, add them to `requirements.user.txt` and install them with `pip install -r requirements.user.txt`.

## Module Conventions

* A module with `urls.py` should declare an `app_name`.
* A module with `urls.py` will have its URLs placed under `/<app_name>/*`.
* A module with a url named `index` in its `urls.py` will have a link to `index` generated in the NetDash navbar.
* A module that generates a permission named `can_view_module` will only generate an `index` link in the NetDash navbar for users who have that permission.
* A module with `api/urls.py` should declare an `app_name`. If the module also has a `urls.py`, it should reuse the previous `app_name` like so: `<app_name>-api`
* A module with `api/urls.py` will have its API URLs placed under `/api/<app_name>/*`.

Check the [example apps](https://github.com/netdash/netdash-examples) examples of these conventions.

## Troubleshooting

If a NetDash Module doesn't properly follow conventions, certain integrations might not work. NetDash includes a `diagnose` command to output information about your NetDash Modules that may assist in refactoring them for inclusion in NetDash.

```
python netdash/manage.py diagnose -v2
```

Will output diagnostics for all NetDash Modules, including any exception traces (`-v2` flag).

If an unrecoverable error is encountered while parsing NetDash Modules, all diagnostics up until the error will be displayed.
