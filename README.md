# NetDash Proof of Concept

## Development

1. Clone this repository.
2. Change to the new directory: `cd netdash`
3. Create a virtualenv: `virtualenv venv`
4. Activate the environment: `source ./venv/bin/activate`
5. Install the package in editable mode: `pip install -e .`
6. Change to the project directory: `cd netdash`
7. Export settings to environment: `export NETDASH_SECRET_KEY=12345 NETDASH_DEBUG=on`
8. If using NetBox export settings to environment: `export NETDASH_DEVICE_MODULE=netdash_device_netbox_api NETBOX_API_URL=http://<netbox>/api`
9. Run the migrations: `python manage.py migrate`
10. Create an admin user: `python manage.py createsuperuser`
11. Run the development server: `python manage.py runserver`
12. Connect to the development server interface: <http://127.0.0.1:8000/>
