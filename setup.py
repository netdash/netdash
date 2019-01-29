from setuptools import setup, find_packages

setup(
    name='netdash',
    version='0.0.0',
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
