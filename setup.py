from os.path import dirname, join
from setuptools import setup, find_packages


with open(join(dirname(__file__), 'src', 'corsa_utils', 'VERSION')) \
        as version_file:
    _version = version_file.read().strip()


setup(
    name='netdash',
    version=_version,
    package_dir={'': 'src'},
    packages=find_packages('src'),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Django ~= 2.2',
        'dj-database-url ~= 0.5.0',
        'djangorestframework ~= 3.9.0',
        'django-rest-swagger ~= 2.2.0',
        'requests ~= 2.20.0',
        'django-cors-headers ~= 2.5.2',
    ],
)
