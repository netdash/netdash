![NetDash](docs/netdash-logo-small.png)

The NetDash project's goal is to create an interface to allow delegation of specific network management tasks to IT teams outside of a central network team. 

[![NetDash Architecture](https://docs.google.com/drawings/d/e/2PACX-1vQEr6ikrwHVAFtjBPgm5zIL8UZib4GsF8H3KgNbUxm5o9MhwRb_vgnz_gG_bUHd03ORH6RiCo2OFFCj/pub?h=800)](https://docs.google.com/drawings/d/1A859k49JQTn8-IcRoAqisa9Si5KzwJtGTJynPENe2cU/edit)

## Development with Docker Compose

1. Install [Docker Compose](https://docs.docker.com/compose/).
2. Clone this repository.
3. Change to the new directory: `cd netdash`
4. `docker-compose up`

This will spin up a few services:
  - NetDash instance (served at 127.0.0.1:8888)
  - NetBox instance (served at 127.0.0.1:8000)
  - Databases for both
  - The NetDash instance is configured by default to use the NetBox instance as its backend.

To change the default settings for the docker-compose setup, create a file in the project root called `.env`. This file is used by Docker Compose to populate its environment. If values are not defined in this file (or your environment), the `docker-compose.yml` file sets default values that will work out of the box.

## Development (Manual)

1. Clone this repository.
2. Change to the new directory: `cd netdash`
3. Create a virtualenv: `virtualenv venv`
4. Activate the environment: `source ./venv/bin/activate`
5. Install the package in editable mode: `pip install -e .`
6. Change to the project directory: `cd src/netdash`
7. Export settings to environment: `export NETDASH_SECRET_KEY=12345 NETDASH_DEBUG=on`
8. If using NetBox export settings from your NetBox instance to environment: `export NETDASH_DEVICE_MODULE=netdash_device_netbox_api NETBOX_API_URL=http://<netbox>/api`
9. Run the migrations: `python manage.py migrate`
10. Create an admin user: `python manage.py createsuperuser`
11. Run the development server: `python manage.py runserver`
12. Connect to the development server interface: <http://127.0.0.1:8000/>

