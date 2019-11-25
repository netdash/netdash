![NetDash](docs/netdash-logo-small.png)

The NetDash project's goal is to create an interface to allow delegation of specific IT infrastructure management tasks to IT teams outside of a central IT team.

This is implemented with a suite of extensible [Django](https://www.djangoproject.com/) apps and core Django project that
seamlessly integrate new modules and customizations without requiring code changes.

With NetDash, you can:
* **Use** the included NetDash Modules out of the box, which are either agnostic to external integrations or generic enough work for most people who have a particular third-party system.
* **Extend** the included NetDash Modules with features and logic meet the needs of your own deployment.
* **Add** completely new NetDash Modules to meet needs that NetDash's included modules do not address.

## Getting Started

Before you get started, completing the [Django Tutorial](https://docs.djangoproject.com/en/2.2/intro/tutorial01/) is recommended to establish a footing in Django apps, development, and project structure.

1. Clone this repository:
    ```
    git clone git@github.com:netdash/netdash.git
    ```
2. Change to the new directory: 
    ```
    cd netdash
    ```
3. Copy the example settings to use them: 
    ```
    cp netdash/netdash/settings_example.py netdash/netdash/settings.py
    ```
4. Install dependencies: 
    ```
    pip install -r requirements.deploy.txt
    ```
5. Run migrations: 
    ```
    python netdash/manage.py migrate
    ```
6. Create a superuser:
    ```
    python netdash/manage.py createsuperuser
    ```
7. Run the development server: 
    ```
    python netdash/manage.py runserver
    ```

You can now visit the interface in your browser at http://localhost:8000. Click 'login' and use your superuser credentials.

## Creating a NetDash Module

A *NetDash Module* is a Django App that follows certain conventions and thereby integrates automatically with NetDash without any additional code changes. These integrations include UI link generation, Swagger API inclusion, routing and permissions.

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

## Module Conventions

* A module with `urls.py` should declare an `app_name`.
* A module with `urls.py` will have its URLs placed under `/<app_name>/*`.
* A module with `urls.py` should have a url named `index`. A link to `index` will be generated in the NetDash navbar.
* A module that generates a permission named `can_view_module` will only generate an `index` link in the NetDash navbar for users who have that permission.
* A module with `api/urls.py` should declare an `app_name`. If the module also has a `urls.py`, it should reuse the previous `app_name` like so: `<app_name>-api`
* A module with `api/urls.py` will have its API URLs placed under `/api/<app_name>/*`.

Check the [example apps](https://github.com/netdash/netdash-examples) for examples of these conventions.

## Troubleshooting

If a NetDash Module doesn't properly follow conventions, certain integrations might not work. NetDash includes a `diagnose` command to output information about your NetDash Modules that may assist in refactoring them for inclusion in NetDash.

```
python netdash/manage.py diagnose -v2
```

Will output diagnostics for all NetDash Modules, including any exception traces (`-v2` flag).

If an unrecoverable error is encountered while parsing NetDash Modules, all diagnostics up until the error will be displayed.

## Deployment Strategies

### Simple: WSGI Server

A common deployment strategy is to copy or clone your NetDash project to a web server and serve it directly via WSGI.
Because NetDash integrates `whitenoise`, you can use `Gunicorn` to serve static content, circumventing the need for an additional web server such as `Apache` or `nginx`.

Pay attention to your deployed `settings.py`. For an example of how to configure NetDash's integrated SAML2 (Shibboleth) support, see `settings_env.py`.

Please see [Deploying Django](https://docs.djangoproject.com/en/2.2/howto/deployment/) for more information on deploying with this method. Pull requests with additional NetDash-specific deployment tips are welcome.

### Advanced: OpenShift/Kubernetes

An institution can deploy their own customized NetDash instance on Kubernetes by:
* Building and pushing a Docker image that extends a [NetDash Dockerhub image](https://hub.docker.com/r/netdash/netdash/tags).
* Creating [`kustomize`](https://kustomize.io/) overlays that extend [`netdash-k8s`](https://github.com/netdash/netdash-k8s).

This is the University of Michigan's preferred method of deploying NetDash. As an example, a high-level overview of the University of Michigan's build picture is as follows:

* Upon pushing a tag (such as `latest` or `beta` or `1.0.0`) to this repository, a CircleCI build is triggered which generates a corresponding [image on Dockerhub](https://hub.docker.com/r/netdash/netdash/tags). These public images can be used by any institution, and have not yet been customized for the University of Michigan.
* The University has a private GitLab repository with `kustomize` overlays (extending `netdash-k8s`) for UMich NetDash environments, as well as a `Dockerfile` for each environment, each extending Dockerhub NetDash images (e.g. `FROM netdash/netdash:beta`). These environment-specific Dockerfiles pull private NetDash Modules from an internal GitLab into the image and install them with `pip`. Developers clone this repository.
* On a developer's machine, secrets are copied from a secure store into the repository's `kustomize` overlay directories, e.g. `overlays/dev/secret`, which are gitignored.
* Kubernetes resources can be created and updated by running e.g. `kustomize build overlays/dev | oc apply -f -` from the developer's local repository.
* One of the created resources is an OpenShift Build. This Build, when triggered, builds environment-specific Docker images from the environment-specific Dockerfiles in the remote repository. It then pushes them to the OpenShift Image Registry, where they can be used by Deployments.
* Secret resources are also generated from the `overlays/dev/secret` directory, which the developer previously populated with secrets. Secrets become environment variables in OpenShift pods. NetDash can reference them through `settings_env.py`.

Additional automation can be achieved using GitLab/GitHub webhooks, OpenShift DeploymentConfig triggers, etc.
