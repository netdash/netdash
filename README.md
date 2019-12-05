![NetDash](docs/netdash-logo-small.png)

[![CircleCI](https://circleci.com/gh/netdash/netdash.svg?style=svg)](https://circleci.com/gh/netdash/netdash)

The NetDash project's goal is to create an interface to allow delegation of specific IT infrastructure management tasks to IT teams outside of a central IT team.

This is implemented with a suite of extensible [Django](https://www.djangoproject.com/) apps and core Django project that
seamlessly integrate new modules and customizations without requiring code changes.

With NetDash, you can:
* **Use** the included NetDash Modules out of the box, which are either agnostic to external integrations or generic enough work for most people who have a particular third-party system.
* **Extend** the included NetDash Modules with features and logic meet the needs of your own deployment.
* **Add** completely new NetDash Modules to meet needs that NetDash's included modules do not address.

## Included Modules

* Host Lookup: Look up device and port information by IP address.
    * `hostlookup-netdisco`: NetDisco backend implementation.
    * `hostlookup-bluecat`: BlueCat backend implementation.
    * `hostlookup-combined`: Combines netdisco and bluecat backends into a single module. Can be easily extended to combine different or additional backends.

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

## NetDash Modules

A *NetDash Module* is a Django App that follows certain conventions and thereby integrates automatically with NetDash without any additional code changes. These integrations include UI link generation, Swagger API inclusion, routing and permissions.

### [Creating a NetDash Module](docs/netdash_modules/creating.md)

### [Module Conventions](docs/netdash_modules/conventions.md)

### [Troubleshooting Modules](docs/netdash_modules/troubleshooting.md)

## Deployment

NetDash can be deployed as a WSGI service or with Kubernetes. See [Deployment Strategies](docs/deployment.md) for more information.
