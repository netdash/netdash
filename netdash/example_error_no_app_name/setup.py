import os
from setuptools import find_packages, setup

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='example-error-no-app-name',
    version='0.0.0',
    packages=find_packages(),
    description='Example NetDash module',
    include_package_data=True,
)
