from setuptools import setup, find_packages

ABOUT = {}
with open('src/netdash/about.py') as fp:
        exec(fp.read(), ABOUT)

setup(
    name=ABOUT['__package_name__'],
    version=ABOUT['__version__'],
    package_dir={'': 'src'},
    packages=find_packages('src'),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Django==2.1.5',
        'dj-database-url==0.5.0',
        'djangorestframework',
        'django-rest-swagger',
        'requests',
    ],
)
