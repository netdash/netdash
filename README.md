# NetDash Proof of Concept

![NetDash Architecture](https://docs.google.com/drawings/d/e/2PACX-1vQEr6ikrwHVAFtjBPgm5zIL8UZib4GsF8H3KgNbUxm5o9MhwRb_vgnz_gG_bUHd03ORH6RiCo2OFFCj/pub?h=800)

## Development

1. Clone this repository. 
2. Change to the new directory: `cd netdash`
3. Create a virtualenv: `virtualenv venv`
4. Activate the environment: `source ./venv/bin/activate`
5. Install the package in editable mode: `pip install -e .`
6. Change to the project directory: `cd src/netdash`
7. Export settings to environment: `export NETDASH_SECRET_KEY=12345 NETDASH_DEBUG=on`
8. Run the migrations: `python manage.py migrate`
9. Create an admin user: `python manage.py createsuperuser`
10. Run the development server: `python manage.py runserver`
11. Connect to the development server interface: <http://127.0.0.1:8000/>

