# Creating a NetDash Module

These steps will turn your local NetDash repository into a development environment for a new NetDash Module. Follow the [Getting Started](docs/index.md) steps if you haven't already.

1. Change directory to NetDash apps: 
    ```
    cd netdash
    ```
2. Create a new NetDash Module, substituting `my_custom_nd_module` for your module's name: 
    ```
    python manage.py startapp --template ../netdash_module_template my_custom_nd_module
    ```
3. To enable your new module, add your module's name to `NETDASH_MODULES` in `netdash/settings.py`:
    ```
    NETDASH_MODULES = [
        'my_custom_nd_module',
    ]
    ```
    NetDash Modules can be specified as Django app labels or as paths to an AppConfig [the same way that `settings.INSTALLED_APPS` is configured](https://docs.djangoproject.com/en/2.2/ref/applications/#for-application-users).
4. Exclude your app from NetDash's source control, substituting `my_custom_nd_module` for your module's name: 
    ```
    echo netdash/my_custom_nd_module >> ../.git/info/exclude
    ```
5. Initialize a git repo in your new NetDash Module's directory: 
    ```
    git init my_custom_nd_module
    ```
6. Run its initial migration: 
    ```
    python manage.py migrate
    ```
7. Restart the development server:
    ```
    python manage.py runserver
    ```

Congrats! You can now explore the interface and look at the NetDash Module you created. If you don't see the module in the interface, make sure you are logged in as your superuser.

If your NetDash Module requires additional packages, add them to `requirements.user.txt` and install them with 
```
pip install -r requirements.user.txt
```
