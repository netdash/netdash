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
        'Django ~= 2.2',
        'dj-database-url ~= 0.5.0',
        'djangorestframework ~= 3.9.0',
        'django-rest-swagger ~= 2.2.0',
        'requests ~= 2.20.0',
    ],
)
